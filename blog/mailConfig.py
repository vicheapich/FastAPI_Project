from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from blog import schemas




conf = ConnectionConfig(
    MAIL_USERNAME = "vicheapich27@gmail.com",
    MAIL_PASSWORD = "qukcbjplraxylrdr",
    MAIL_FROM = "vicheapich27@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Vichea Pich",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,   
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def send_email(user_email: schemas.ForgotPassword, html):
    message = MessageSchema(
        subject="Code verify for Reset password Token",
        recipients = user_email,
        body = html,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)