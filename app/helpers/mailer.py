from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from pathlib import Path  # For reading HTML template
import jinja2,base64
import dotenv
import os
import logging
from urllib.parse import urljoin
# load env vars
dotenv.load_dotenv()

class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),  # Use 587 for StartTLS)
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,  # Enable StartTLS
    MAIL_SSL_TLS=False,  # Disable SSL/TLS
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False
)
# print(conf.dict())

def render_html_template(template_file: str,name:str, code: str) -> str:
    template_loader = jinja2.FileSystemLoader(searchpath="templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_file)
    rendered_template = template.render(code=code,name=name)
    return rendered_template



async def send_email_verification_otp(user):
    """Send an OTP for email verification when a user signs up."""
    
    message = MessageSchema(
        subject="Intranet Email Verification",
        recipients=[user.email],
        body=f"""
        Hello {user.name},

        Welcome to the Intranet!

        Please use the following One-Time Password (OTP) to verify your email address:

        **{user.email_verification_token}**

        This OTP is valid for 10 minutes . If you did not sign up for a Intranet account, please ignore this email.

        Regards,  
        Management Team
        """,
        subtype="plain",
    )

    fm = FastMail(conf)

    try:
        await fm.send_message(message)
        logging.info(f"Email verification OTP sent to {user.email}")
    except Exception as e:
        logging.error(f"Error sending OTP email to {user.email}: {e}")
        raise

async def send_forgot_password_otp(name,email, otp):
    """Send a password reset link via email."""
    
    message = MessageSchema(
        subject="Intranet Password Reset OTP",
        recipients=[email],
        body=f"""
        Hello {name},

        We received a request to reset your password.
        
        Please use the following One-Time Password (OTP) to reset your password:

        **{otp}**

        This OTP is valid for 10 minutes . If you did not make this, please ignore this email.

        Regards,  
        Management Team
        """,
        subtype="plain",
    )

    fm = FastMail(conf)

    try:
        await fm.send_message(message)
        logging.info(f"PASSWORD RESET OTP SENT TO {email}")
    except Exception as e:
        logging.error(f"ERROR SENDING FORGOT PASS OTP TO {email}: {e}")
        raise

async def send_login_otp(name,email, otp):
    """Send login otp."""
    
    message = MessageSchema(
        subject="Intranet Login OTP",
        recipients=[email],
        body=f"""
        Hello {name},
        
        Please use the following One-Time Password (OTP) to login to the system:

        **{otp}**

        This OTP is valid for 10 minutes . If you did not make this, please ignore this email.

        Regards,  
        Management Team
        """,
        subtype="plain",
    )

    fm = FastMail(conf)

    try:
        await fm.send_message(message)
        logging.info(f"PASSWORD RESET OTP SENT TO {email}")
    except Exception as e:
        logging.error(f"ERROR SENDING FORGOT PASS OTP TO {email}: {e}")
        raise
