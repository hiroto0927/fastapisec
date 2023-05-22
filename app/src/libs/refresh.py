import jwt
import os
from fastapi import Depends
from src.db.database import get_db
from dotenv import load_dotenv
from src.schemas.auth import RefreshDecoded
from sqlalchemy.orm import Session
from src.libs import hashed
from src.models.refresh import Refresh
from src.libs import token
from datetime import datetime, timedelta

load_dotenv()

PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def encode_jwt(data: dict):
    to_encode = data.copy()

    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decoded_refresh_token(encoded_refresh: str) -> RefreshDecoded:
    decoded_refresh = jwt.decode(encoded_refresh, PUBLIC_KEY, algorithms=ALGORITHM)

    response = RefreshDecoded(
        sub=decoded_refresh["sub"],
        kid=decoded_refresh["kid"],
        iat=decoded_refresh["iat"],
        exp=decoded_refresh["exp"],
    )

    return response


def create_refresh_token(user_id: int, db: Session):
    kid: str = hashed.randomstr(10)

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

    refresh_token = token.create_refresh_token(
        data={
            "sub": user_id,
            "kid": kid,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=30),
        }
    )

    return refresh_token
