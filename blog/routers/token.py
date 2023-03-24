from datetime import datetime, timedelta
from jose import JWTError, jwt
from .. import schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 #a day

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(data: str, credentials_exception):
    try:
        payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
def create_refresh_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_Jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_Jwt


# from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# fernet = Fernet(key)


# # Function to encrypt a key
# def encrypt_key(plain_key:str):
#     plain_bytes = bytes(plain_key, 'utf-8')
#     encrypted_bytes = fernet.encrypt(plain_bytes)
#     encrypted_key = encrypted_bytes.decode('utf-8')
#     return encrypted_key

# # Function to decrypt a key
# def decrypt_key(encrypted_key: str):
#     encrypted_bytes = bytes(encrypted_key, 'utf-8')
#     decrypted_bytes = fernet.decrypt(encrypted_bytes)
#     plain_key = decrypted_bytes.decode('utf-8')
#     return plain_key