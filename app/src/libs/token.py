from datetime import datetime, timedelta
from fastapi import Depends,Response
from typing import Union
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.user import User
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from src.schemas.auth import AuthUser
from jose.exceptions import ExpiredSignatureError

load_dotenv()

PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def create_access_token(data: dict):
    to_encode = data.copy()

    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def decode_access_token(encoded_jwt:str):
    try:
        decoded_token = jwt.decode(encoded_jwt, PRIVATE_KEY, algorithms=ALGORITHM)
        return decoded_token
    except ExpiredSignatureError:
        raise HTTPException(401,'ExpiredSignatureError')
    except JWTError:
        raise HTTPException(401)

def get_cuurent_user(credential: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credential.credentials
    decoded_token = decode_access_token(token)

    return decoded_token
