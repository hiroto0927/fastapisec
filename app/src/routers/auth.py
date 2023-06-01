from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas.auth import Create
from fastapi import HTTPException
from src.models.user import User
from src.models.refresh import Refresh
from src.schemas.jwt import PublicKey, Refresh as RefreshSchema, Token
from dotenv import load_dotenv
import os
from datetime import datetime
from src.libs import pwd, jwt


load_dotenv()


ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
kty = os.environ.get("kty")
n = os.environ.get("n")
e = os.environ.get("e")


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/token", response_model=Token)
def create_user(req: Create, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()

    if user is None:
        raise HTTPException(404, "user is not found")

    if pwd.check_password(user.salt + req.password, user.hashedpass) == False:
        raise HTTPException(401, "Invalid credentials")

    access_token = jwt.create_access_token(user.email)

    refresh_token = jwt.create_refresh_token(user.id, db)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/public-key", response_model=PublicKey)
def publish_public_key():
    return {"kty": kty, "n": n, "e": e}


@router.post("/refresh-token", response_model=Token)
def refresh_publish(req: RefreshSchema, db: Session = Depends(get_db)):
    decoded = jwt.decoded_refresh_token(req.refresh_token)

    if int(datetime.utcnow().timestamp()) > decoded.exp:
        raise HTTPException(401, "JWT is already expired.")

    valid_refresh = db.query(Refresh).filter(Refresh.id == decoded.sub)

    if valid_refresh.first() is None:
        raise HTTPException(401, "Invalid credentials")

    if valid_refresh.filter(Refresh.kid == decoded.kid).first() is None:
        raise HTTPException(401, "Invalid credentials")

    user = db.query(User).filter(User.id == decoded.sub).first()

    access_token = jwt.create_access_token(user.email)

    refresh_token = jwt.create_refresh_token(user.id, db)

    return {"access_token": access_token, "refresh_token": refresh_token}
