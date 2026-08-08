from fastapi_mail import FastMail, MessageSchema, MessageType
from app.config.email_config import email_config


async def send_otp_email(to_email:str, otp:str):
    message= MessageSchema(
        subject="Your OTP Code",
        recipients=[to_email],
        body=f"Your OTP Code is: {otp}\nThis code will expire in 10 minutes.",
        subtype=MessageType.plain
    )
    fm = FastMail(email_config)
    await fm.send_message(message)
