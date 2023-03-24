from pydantic import BaseModel, EmailStr
from typing import List, Optional

class BlogBase(BaseModel):
    title : str
    body  : str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class User(BaseModel):
    name:str
    email:str
    password:str
    phone:str
    birth_of_date:str

class ShowUser(BaseModel):
    name:str
    email:str
    blogs : List['Blog']=[]
    class Config():
        orm_mode = True

class ShowBlog(Blog):
    title : str
    body : str
    creator : ShowUser
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    email:Optional[str]

class ForgotPassword(BaseModel):
    email:str

class ResetPassword(BaseModel):
    reset_password_token:str
    new_password:str
    confirm_password:str

class UpdateProfile(BaseModel):
    name:str

class ChangPassword(BaseModel):
    current_password:str
    new_password:str
    confirm_password:str

class UserCreate(User):
    password:str

class CreateOTP(BaseModel):
    recipient_id:str

class VerifyOTP(BaseModel):
    recipient_id:str
    session_id:str
    otp_code:str

class OTPList(VerifyOTP):
    otp_failed_count:int
    status : str

class Email(BaseModel):
    email : List[EmailStr]
