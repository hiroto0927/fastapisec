import random, string
from passlib.context import CryptContext
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends
from src.libs import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def randomstr(n: int):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))


def get_password_hashed(password: str, salt: str):
    return pwd_context.hash(salt + password)


def check_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_cuurent_user(credential: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credential.credentials
    decoded_token = jwt.decode_access_token(token)
    print(decoded_token)
    return decoded_token
