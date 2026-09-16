import os
import mysql.connector
from datetime import timezone
from dotenv import load_dotenv
from mysql.connector import Error
from email.utils import parsedate_to_datetime

load_dotenv()

Db_Host = os.getenv("DB_HOST")
Db_Port = os.getenv("DB_PORT")
Db_User = os.getenv("DB_USER")
Db_Password = os.getenv("DB_PASSWORD")
DataBase_Name = os.getenv("DB_NAME")

def convert_date_sql(data: dict):
    """ convert the date to make the date compatible for sql data """

    date_str = data["Date"]
    
    dt = parsedate_to_datetime(date_str)      
    dt_utc = dt.astimezone(timezone.utc)      
    dt_naive = dt_utc.replace(tzinfo=None)
    
    data['Date'] = dt_naive

    return data

def get_connection():
    try:
        conn = mysql.connector.connect(
                    host = Db_Host,
                    port = Db_Port,
                    user = Db_User,
                    password = Db_Password,
                    database = DataBase_Name
                )
        return conn
    except Error as e:
        print(f"Failed to connect to MySQL:{e}")
        raise

def Mail_data():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""         
            CREATE TABLE IF NOT EXISTS emails (
                messageid VARCHAR(255) PRIMARY KEY,
                sender VARCHAR(255),
                subject VARCHAR(500),
                date DATETIME)
                """)
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise
    finally: 
        cursor.close()
        conn.close()

def init_db():
    Mail_data()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
    # Creating Summary Table
        cursor.execute("""         
               CREATE TABLE IF NOT EXISTS Summary_Mail (
                   messageid VARCHAR(255) PRIMARY KEY,
                   Summary MEDIUMTEXT,
                   Purpose MEDIUMTEXT,
                   Reply VARCHAR(5) ) 
                """)
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise
    finally: 
        cursor.close()
        conn.close()

def insert_details(mail, Data):
    init_db()  
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute(" SELECT messageid FROM emails WHERE messageid = %s", 
                       (mail["Message_id"],))
        
        exists = cursor.fetchone()
        
        sql1 = """INSERT INTO emails (messageid, sender, subject, date)
                   VALUES (%s, %s, %s, %s)"""
        
        if not exists:
            cursor.execute( sql1,
                (mail["Message_id"], mail["From"], mail["Subject"], mail["Date"])
          )
           
        cursor.execute("SELECT messageid FROM Summary_Mail WHERE messageid = %s", (mail["Message_id"],))
        
        exists2 = cursor.fetchone()
        
        sql2 = """INSERT INTO Summary_Mail (messageid, Summary, Purpose, Reply)
                   VALUES (%s, %s,%s, %s)"""
        if not exists2:
            cursor.execute( sql2,
                    (mail["Message_id"], Data.summary, Data.purpose, Data.reply)
               )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()  

def fetch_mail_db(messageid):
    """ fetch the data from the summary table if exists """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try: 
        fetch_data = """ SELECT * FROM Summary_Mail WHERE messageid = %s """ 
        cursor.execute(fetch_data, (messageid,))
        data = cursor.fetchone()
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise
        
    finally: 
        cursor.close()
        conn.close()

    return data
    