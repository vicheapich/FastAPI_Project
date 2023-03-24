from fastapi import APIRouter, HTTPException, Depends, status
from blog import database, mailConfig
from blog.routers import oauth2
from ..respository import user
from .. import enumotp,schemas
from sqlalchemy.orm import Session
from ..respository import otp
import uuid




router = APIRouter(
    tags = ['OTPs']
)

#Sent OTP to user by vichea (not yet)
@router.post('/sent_otp')
async def send_otp(type: enumotp.OTPType ,request: schemas.CreateOTP , db:Session = Depends(database.get_db)):

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
    """.format(request.recipient_id, otp_code)
    user_verify_email = []
    user_verify_email.append(request.recipient_id)
    await mailConfig.send_email(user_verify_email, html)

    #check user input type is Phone
    if type == enumotp.OTPType.Phone:

        #check user or not
        check_user = user.find_user_by_phone(request.recipient_id, db)
        if not check_user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"User Not Found")
        
        # check block OTP
        otp_block = otp.find_otp_block(request.recipient_id, db)
        if otp_block:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sorry, this phone number is blocked in 5 minutes")
        
        #Generate and save it to table otps
        otp_code = otp.random(6)
        session_id = str(uuid.uuid1())
        otp.save_otp(request.recipient_id , session_id, otp_code , db)

        return {"message":"Sorry, We're unavailable with this fuction."}
        # return {
        #     "recipient_id"  :   request.recipient_id,
        #     "session_id"    :   session_id,
        #     "otp_code"      :   otp_code,
        #     "message"       :   "OTP sent Successfully."
        # }
    
    #check user input type is Email
    elif type == enumotp.OTPType.Email:
        #check user or not
        check_user = user.find_exit_user(request.recipient_id, db)
        if not check_user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"User Not Found")
        
        # check block OTP
        otp_block = otp.find_otp_block(request.recipient_id, db)
        if otp_block:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sorry, this phone number is blocked in 5 minutes")
        
        #Generate and save it to table otps
        otp_code = otp.random(6)
        session_id = str(uuid.uuid1())
        otp.save_otp(request.recipient_id , session_id, otp_code , db)

        return {
            "recipient_id"  :   request.recipient_id,
            "session_id"    :   session_id,
            "otp_code"      :   otp_code,
            "message"       :   "OTP sent Successfully."
        }

#verify user's otp with system's otp by vichea (done)
@router.post('/verify_otp')
async def verify_otp(request: schemas.VerifyOTP, db:Session = Depends(database.get_db)):
    #check block OTP
    otp_block = otp.find_otp_block(request.recipient_id, db)
    if otp_block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" Sorry, this phone number is blocked in 5 minutes")
    
    #check OTP code 6 digits lifetime
    lifetime_result = otp.find_otp_lifetime(request.recipient_id, request.session_id, db)


    #OTP already used
    if lifetime_result.status == "9":
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f" OTP has used, please request a new one.")
    
    if lifetime_result.otp_code != request.otp_code:
        otp.update_otp_failed_count(lifetime_result.recipient_id, lifetime_result.session_id, lifetime_result.otp_code, lifetime_result.otp_failed_count, db)
        if lifetime_result.otp_failed_count == 5:
            otp.save_block_otp(lifetime_result.recipient_id ,db)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" Sorry, this phone number is blocked in 5 minutes")
        
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f" The OTP code you have entered is incorred.")
    otp.disable_otp_code(lifetime_result.recipient_id, lifetime_result.session_id, lifetime_result.otp_code, db)

    return {
        "status_code " : status.HTTP_200_OK,
        "message" : "OTP verified Successfully."
    }