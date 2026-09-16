from fastapi import FastAPI
from summarizer import graph_call
from fastapi.middleware.cors import CORSMiddleware
from email_fetch import fetch_mail_exetension, extract_mail
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
) 
   
@app.get('/')
def welcome():
    return {"message": "Welcome to the email summarizer api. Have a good day!"}

@app.post('/email')
async def receive_data(data: dict):

    mail_data = fetch_mail_exetension(data)

    checker = mail_data.get("Summary")
    if checker:
        return mail_data
    else:
        llm = graph_call(mail_data)
        return llm
