import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from jwt.exceptions import PyJWTError, ExpiredSignatureError
from src.schemas.jwt import RefreshDecoded
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models.refresh import Refresh
from src.libs import pwd

load_dotenv()

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def create_access_token(email: str):
    to_encode: dict = {
        "sub": email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }

    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(encoded_jwt: str):
    try:
        decoded_token = jwt.decode(encoded_jwt, PUBLIC_KEY, algorithms=ALGORITHM)
        return decoded_token
    except ExpiredSignatureError:
        raise HTTPException(401, "ExpiredSignatureError")
    except PyJWTError:
        raise HTTPException(401, "JWT Error")


def create_refresh_token(user_id: int, db: Session):
    kid: str = pwd.randomstr(10)

    refresh = db.query(Refresh).filter(Refresh.id == user_id)

    if refresh.first() is None:
        token_data = Refresh()
        token_data.id = user_id
        token_data.kid = kid
        db.add(token_data)
        db.commit()
    else:
        refresh.update({"kid": kid})
        db.commit()

    to_encode: dict = {
        "sub": user_id,
        "kid": kid,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }

    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decoded_refresh_token(encoded_refresh: str):
    decoded_refresh = jwt.decode(encoded_refresh, PUBLIC_KEY, algorithms=ALGORITHM)

    response = RefreshDecoded(
        sub=decoded_refresh["sub"],
        kid=decoded_refresh["kid"],
        iat=decoded_refresh["iat"],
        exp=decoded_refresh["exp"],
    )

    return response
