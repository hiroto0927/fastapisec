from fastapi import Depends
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose.exceptions import ExpiredSignatureError

load_dotenv()

PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def create_access_token(data: dict):
    to_encode = data.copy()

    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()

    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(encoded_jwt: str):
    try:
        decoded_token = jwt.decode(encoded_jwt, PUBLIC_KEY, algorithms=ALGORITHM)
        return decoded_token
    except ExpiredSignatureError:
        raise HTTPException(401, "ExpiredSignatureError")
    except JWTError:
        raise HTTPException(401)


def decode_refresh_token(encoded_refresh: str):
    try:
        decoded_refresh = jwt.decode(encoded_refresh, PUBLIC_KEY, algorithms=ALGORITHM)
        return decoded_refresh
    except ExpiredSignatureError:
        raise HTTPException(401, "ExpiredSignatureError")
    except JWTError:
        raise HTTPException(401)


def get_cuurent_user(credential: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credential.credentials
    decoded_token = decode_access_token(token)

    return decoded_token
