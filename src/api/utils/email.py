from fastapi import BackgroundTasks, UploadFile, File, Form, FastAPI, HTTPException, Depends ,status
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig,MessageType
from ..schemas.email import Email as EmailSchema
from ..schemas.user import User
import os


conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True
)

html = """
<p>Thanks for using Fastapi-mail</p> 
"""

async def send_email(email: EmailSchema):
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.model_dump().get("email"),
        body=html,
        subtype=MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}
