from datetime import datetime, timedelta
import pytz
from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from .. import models, schemas, hashing


def create(db:Session, request:schemas.User):
    new_user = models.User(
        name = request.name,
        email=request.email,
        password = hashing.Hash.bcrypt(request.password),
        phone = request.phone,
        birth_of_date = request.birth_of_date,
        status = "1",
        create_on = datetime.now(pytz.timezone('Asia/Phnom_Penh'))
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id:int, db:Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not available")
    return user

def find_black_list_token(token:str, db:Session):
    used_token = db.query(models.Blacklist).filter(models.Blacklist.token == token).first()
    return used_token

def save_black_list_token(token:str, db:Session, current_user = models.User.email):
    block_token = models.Blacklist(token = token, email=current_user)
    db.add(block_token)
    db.commit()
    db.refresh(block_token)
    return block_token

def find_exit_user(email:str, db:Session):
    user_exit = db.query(models.User).filter(models.User.email ==email).first()
    if not user_exit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    return user_exit

def find_user_by_phone(phone:str , db:Session):
    user_exit = db.query(models.User).filter(models.User.phone == phone).first()
    if not user_exit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    return user_exit

def create_reset_code(email:str ,reset_code: str , db:Session):
    resetcode = models.Code(email = email , reset_code = reset_code , expired_in = datetime.now(pytz.timezone('Asia/Phnom_Penh')))
    db.add(resetcode)
    db.commit()
    db.refresh(resetcode)
    return resetcode

def check_reset_password_token(reset_password_token:str, db:Session):
    password_token =  db.query(models.Code).filter(and_(models.Code.reset_code == reset_password_token, models.Code.expired_in  >= datetime.now(pytz.timezone('Asia/Phnom_Penh')) - timedelta(minutes= 1))).first()
    return password_token

def reset_password(new_hashed_password:str , email:str, db:Session):
    password_reset = db.query(models.User).filter(models.User.email == email)
    if not password_reset.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not found")
    password_reset.update({"password":new_hashed_password})
    db.commit()
    return "password has been update."

def update_profile(name:str, email:str ,db:Session):
    update_p = db.query(models.User).filter(models.User.email == email)
    if not update_p.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not Found")
    update_p.update({"name":name})
    db.commit()
    return "Update"

def delete_user(email:str, db:Session):
    delete_acc = db.query(models.User).filter(models.User.email == email)
    if not delete_acc.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    delete_acc.delete(synchronize_session=False)
    db.commit()
    return "Done"

def change_password(new_password:str, email:str, db:Session):
    update_pwd = db.query(models.User).filter(models.User.email == email)
    if not update_pwd.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not Found")
    update_pwd.update({"password":new_password})
    db.commit()
    return "Changed"