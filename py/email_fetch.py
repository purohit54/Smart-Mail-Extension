import os
import email
from imaplib import IMAP4_SSL
from dotenv import load_dotenv
from db import convert_date_sql, get_connection, Mail_data, init_db, insert_details, fetch_mail_db


load_dotenv()

Email_Address = os.getenv("EMAIL_ADDRESS")
Email_Password = os.getenv("EMAIL_PASSWORD")


def connect():
    mail = IMAP4_SSL(host = "imap.gmail.com", port = 993)
    mail.login(Email_Address, Email_Password)
    return mail



def extract_mail(mail_data):
    """ This function extract mail data for the given mail id  """

    attachment_names = []
    # create the name of the folder in current folder
    attachment_paths = "Attachments"
    os.makedirs(attachment_paths, exist_ok=True)
    datas = {}
    for response_part in mail_data: # it is taking one part from the mail
        if isinstance(response_part, tuple):

            msg = email.message_from_bytes(response_part[1])
            data = fetch_mail_db(msg['Message-ID'])
                        
            if data:
                return data
            else:
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        filename = part.get_filename()
                            
                        if content_type == "text/plain":
                        
                            body = part.get_payload(decode=True).decode('utf-8', errors = 'ignore')
                            body_content = body
                                                  
                        if filename:
                            print(f"Found attachment: {filename}")
                            attachment_names.append(filename)
                            
                            file_data = part.get_payload(decode = True)
                             
                            file_path = os.path.join(attachment_paths, filename)
                               
                            with open(file_path, "wb") as f:
                                f.write(file_data)
                else:
                    content_type = msg.get_content_type()
                    if content_type == "text/plain":
                        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                        body_content = body
                
                # print("Data from extract mail function line 88 in email_fetch file", msg["FROM"])

                data_a = {
                    'From': msg["FROM"],
                    'To': msg["TO"],
                    'cc': msg["cc"],
                    'Subject': msg["Subject"],
                    'Date': msg["Date"],
                    'Message_id': msg["Message-ID"],
                    'body_content': body_content,
                    'attachments': attachment_names,
                    }
            
                new_data = convert_date_sql(data_a)
                datas = new_data.copy()
                return datas

def fetch_mail_exetension(email: dict):
    """ Fetches mail id for the opened mail on webpage """

    mail = connect()
    mail.select("INBOX")
    mail._encoding = "utf-8"
    subject = (email['subject']
    .replace("“", '"')
    .replace("”", '"'))
    status2, data = mail.search(None,f'SUBJECT "{subject}"')
    
    mail_ids = data[0].split()

    print("STATUS2:", status2)
    print("MESSAGES2:", mail_ids)
    print("MESSAGES2 Length:", len(mail_ids))

    if(len(mail_ids) != 1):
        status, data2 = mail.search(None, 'FROM', email['from'], 'SUBJECT', email['subject'], 'BODY', email['body'])
        ids = data2[0].split()

        if (len(ids) == 1):
            status, mail_data = mail.fetch(ids[0], '(RFC822)')
            mail = extract_mail(mail_data)
            return mail
        else:
            print("Unable to find to find opened mail with backend")
    else:
        status, mail_data = mail.fetch(mail_ids[0], '(RFC822)')
        mail = extract_mail(mail_data)
        return mail
    
