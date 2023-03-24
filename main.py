# from typing import Union

# from typing import Optional

# from fastapi import FastAPI

# from pydantic import BaseModel

# app = FastAPI()

# class Blog(BaseModel):
#     title  : str
#     body   : str
#     published : Optional[bool]
# @app.get("/")

# def read_root():

#     return {"Hello": "World"}

# @app.get("/blog/{id}/comment")

# def comment(id, limit=5):

#     return {'data':{'1','2','3','4','5','6','7','8'}}



from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    # MAIL_USERNAME = "vichea",
    MAIL_PASSWORD = "x p g c a b c a c f f u l b o m",
    # MAIL_PASSWORD = "uxisabcojfmslsab",
    # MAIL_FROM = "vichea@email.com",
    MAIL_FROM= "sarathorn27@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    # MAIL_FROM_NAME="vichea",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

app = FastAPI()

@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})