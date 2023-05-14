from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas.auth import Create
from fastapi import HTTPException
from src.models.user import User
from src.libs import hashed,token
from src.schemas.auth import Read
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

router = APIRouter(prefix="/api/auth/login",tags=["auth"])


@router.post("/",response_model=Read)
def create_user(req:Create,db:Session = Depends(get_db)):

    user = db.query(User).filter(User.email == req.email).first()

    if user == None:
        raise HTTPException(404,'user not found')

    if hashed.check_password(user.salt+req.password,user.hashedpass) == False:
        raise HTTPException(401,"Invalid credentials")

    access_token_expires = timedelta(minutes=30)
    access_token = token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token,"token_type": "bearer"}