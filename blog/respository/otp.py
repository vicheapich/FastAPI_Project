from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from blog import schemas
from .. import models
from sqlalchemy import and_
import pytz
import string
from random import choice


def find_otp_block(recipient_id:str , db:Session):
    block_num = db.query(models.Optblocks).filter(and_(models.Optblocks.recipient_id == recipient_id, models.Optblocks.create_on >= datetime.now(pytz.timezone('Asia/Phnom_Penh')) - timedelta(minutes= 5))).first()
    return block_num

def random(digits: int):
    num = string.digits
    return "".join(choice(num) for _ in range(digits))

def save_otp(recipient_id:str , session_id:str , otp_code:int , db:Session):
    code_otp = models.Otps(recipient_id = recipient_id , session_id = session_id, otp_code = otp_code, status = 1 ,create_on = datetime.now(pytz.timezone('Asia/Phnom_Penh')))
    db.add(code_otp)
    db.commit()
    db.refresh(code_otp)
    return code_otp

def find_otp_lifetime(recipient_id:str, Session_id:str , db:Session):
    code_otp = db.query(models.Otps).filter(models.Otps.recipient_id == recipient_id, models.Otps.session_id == Session_id , models.Otps.create_on  >= datetime.now(pytz.timezone('Asia/Phnom_Penh')) - timedelta(minutes= 5)).first()
    if not code_otp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"OTP has used, please request a new one.")
    return code_otp

def update_otp_failed_count(recipient_id: str, Session_id : str, otp_code:str , otp_failed_count:int,  db:Session):
    count = db.query(models.Otps).filter(models.Otps.recipient_id == recipient_id, models.Otps.session_id== Session_id, models.Otps.otp_code == otp_code)
    if not count.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found")
    count.update({'otp_failed_count':otp_failed_count + 1})
    db.commit()
    return "DONE"

def save_block_otp(recipient_id:str ,db:Session):
    saveotp = models.Optblocks(recipient_id= recipient_id, create_on = datetime.now(pytz.timezone('Asia/Phnom_Penh')))
    db.add(saveotp)
    db.commit()
    db.refresh(saveotp)
    return saveotp

def disable_otp_code(recipient_id: str, Session_id : str, otp_code:str , db:Session):
    count = db.query(models.Otps).filter(models.Otps.recipient_id == recipient_id, models.Otps.session_id==Session_id, models.Otps.otp_code == otp_code)
    if not count.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found")
    status_code = 9
    count.update({'status': status_code})
    db.commit()
    return "DONE"
