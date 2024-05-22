from fastapi import BackgroundTasks, UploadFile, File, Form, FastAPI, HTTPException, Depends ,status
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig,MessageType
from ..schemas.email import Email as EmailSchema
from ..schemas.user import User
import os
from pathlib import Path




conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    TEMPLATE_FOLDER= Path(__file__).parent/'templates/'
)


async def send_email(email: EmailSchema,template:str="verification.html",subject:str="GestPlay",body:dict={"link":"https://gestplay.com"}):
    message = MessageSchema(
        subject=subject,
        recipients=email.model_dump().get("email"),
        template_body=body,
        subtype=MessageType.html)
    fm = FastMail(conf)
    try:
        await fm.send_message(message, template_name=template)
        return True
    except ConnectionError as e:
        # print(e)
        return False