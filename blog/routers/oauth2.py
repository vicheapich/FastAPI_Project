from fastapi import Depends, Request, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from blog import database
from .. import models, schemas
from fastapi.security import OAuth2PasswordBearer
from .import token
from ..respository import user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(data: str = Depends(oauth2_scheme), db: database.SessionLocal = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #check blacklist token
    used_black_list = user.find_black_list_token(data, db)
    if used_black_list:
        raise credentials_exception

    return token.verify_token(data, credentials_exception)

def get_token_user(token:str = Depends(oauth2_scheme)):
    return token

# def get_current_active_user(request: Request):
#     current_user = request.cookies.get("username")
#     if not current_user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")

####
async def get_login_user(data: str = Depends(oauth2_scheme), db: database.SessionLocal = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(data, token.SECRET_KEY, algorithms=[token.ALGORITHM])
        email: str = payload.get("sub")
      
        if email is None:
            raise credentials_exception
        token_data = user.find_exit_user(email, db)
    
        if not token_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
        return token_data
    except JWTError:
        raise credentials_exception