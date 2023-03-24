from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi import APIRouter,Depends, HTTPException, Request, Response, status
from blog.routers import oauth2
from .. import schemas, database, models, mailConfig
from sqlalchemy.orm import Session
from ..hashing import Hash
from . import token
import uuid


router = APIRouter(
    tags = ['Authentication']
)


@router.post('/login')
def login(response: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    response.set_cookie(key="username", value=user.email)
    response.set_cookie(key="userid", value=user.id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"USER is NOT FOUND.")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"Incorrect Password.")

    
    access_token = token.create_access_token(data={"sub": user.email})
    refresh_token = token.create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token ,"token_type": "bearer"}

@router.get('/refresh')
def refresh(request:Request):
    current_user = request.cookies.get("username")
    refresh_token = token.create_access_token(data={"sub": current_user})
    return {"access_token":refresh_token ,"token_type": "bearer"}

from ..respository import user
@router.get("/logout")
async def logout(request: Request ,token:str = Depends(oauth2.get_token_user), db: database.SessionLocal = Depends(database.get_db)):
    current_user = request.cookies.get("username")
    user.save_black_list_token(token ,db, current_user)
    return {
        "status_code ": status.HTTP_200_OK,
        "detail":"User logged out successfully."
    }

@router.post("/forgot_password", )
async def forgot_password(request: schemas.ForgotPassword = Depends(), db: Session = Depends(database.get_db)):
    #check user exits 
    users = user.find_exit_user(request.email ,db)
    if not users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"USER is NOT FOUND.")
    
    #Create reset code and save into database
    reset_code = str(uuid.uuid1())
    user.create_reset_code(request.email, reset_code, db)

    #Sending Email
    html = """
        <!DOCTYPE html>
            <html>
                <body>
                    <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
                        <div style="margin:50px auto;width:70%;padding:20px 0">
                            <div style="border-bottom:1px solid #eee">
                                <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">ZFS FastAPI</a>
                            </div>
                                <p style="font-size:1.1em">Hi {0},</p>
                                <p>Thank you for choosing ours ZFS service. Use the following Token to complete your reset procedures. Token is valid for 5 minutes</p>
                                <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{1}</h2>
                                <p style="font-size:0.9em;">Regards,<br />Your Brand</p>
                                <hr style="border:none;border-top:1px solid #eee" />
                            <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
                                <p>ZFS Inc</p>
                                <p>N012, 12st, Phnom Penh</p>
                                <p>Cambodia</p>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
    """.format(request.email, reset_code)
    user_verify_email = []
    email = request.email
    user_verify_email.append(email)
    await mailConfig.send_email(user_verify_email, html)
    return {
        "status_code " : status.HTTP_200_OK,
        "message" : "Sent Successfully."
    }

@router.post("/reset-password")
async def reset_password(request: schemas.ResetPassword,  db: Session = Depends(database.get_db)):
    #check valid reset password token
    reset_token = user.check_reset_password_token(request.reset_password_token, db)
    if not reset_token:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f" Reset password has expired, please request a new one.")
    
    #check both new & comfirm password are matched
    if request.new_password != request.confirm_password:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"New password isn't match.")
    

    #reset New password
    new_hashed_password = Hash.bcrypt(request.new_password)
    user.reset_password(new_hashed_password, reset_token.email , db)

    return {
        "status_code " : status.HTTP_200_OK,
        "message" : "Password has been reset Successfully."
    }

@router.patch("/change-password")
async def change_password(request:schemas.ChangPassword, db:Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_login_user)):
    check_user = user.find_exit_user(current_user.email, db)
    if not check_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"User Not Found")
    
    #verify current password
    check_current_password = Hash.verify(check_user.password,request.current_password)
    if not check_current_password:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"Invaild with current password.")
    #check strong password 
    
    #compare password
    if request.new_password != request.confirm_password:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"New password isn't match.")
    
    #set new password
    new_hashed_password = Hash.bcrypt(request.new_password)
    user.change_password(new_hashed_password , current_user.email, db)
    return {
        "status_code " : status.HTTP_200_OK,
        "message" : "Password has been reset Successfully."
    }