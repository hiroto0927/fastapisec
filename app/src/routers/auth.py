from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas.auth import Create
from fastapi import HTTPException
from src.schemas.jwt import PublicKey, Refresh as RefreshSchema, Token, DeleteRefresh, DeleteResponse
import os
from jwt import ExpiredSignatureError, InvalidTokenError
from src.utils.exeption import PasswordNotMatchError, NotUserExistException
from src.cruds import auth
from dotenv import load_dotenv
from src.libs import jwt

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/token", response_model=Token)
def create_token(req: Create, db: Session = Depends(get_db)):
    try:
        return auth.create_token_by_email(req, db)
    except NotUserExistException:
        raise HTTPException(404, "Not Found User")
    except PasswordNotMatchError:
        raise HTTPException(401, "Invalid credentials")


@router.get("/public-key", response_model=PublicKey)
def publish_public_key():
    key = jwt.create_public_key_to_jwk()
    return key


@router.post("/refresh-token", response_model=Token)
def refresh_publish(req: RefreshSchema, db: Session = Depends(get_db)):
    try:
        return auth.token_republish_by_refresh_token(req, db)
    except ExpiredSignatureError:
        raise HTTPException(401, "Signature has expired")
    except InvalidTokenError:
        raise HTTPException(401, "Invalid credentials")


@router.delete("/refresh-token", response_model=DeleteResponse)
def delete_refresh_token(req: DeleteRefresh, db: Session = Depends(get_db)):
    try:
        return auth.delete_refresh_token_by_email(req, db)
    except NotUserExistException:
        raise HTTPException(404, "Not Found User")
    except InvalidTokenError:
        raise HTTPException(401, "Invalid credentials")
