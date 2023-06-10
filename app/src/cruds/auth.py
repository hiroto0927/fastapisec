from sqlalchemy.orm import Session
from src.models.user import User
from src.libs import jwt, pwd
from src.schemas.auth import Create
from src.schemas.jwt import Refresh as RefreshSchema
from src.utils.exeption import NotFoundException, PasswordNotMatchError, NotUserExistException
from datetime import datetime
from src.models.refresh import Refresh
from jwt import ExpiredSignatureError, InvalidTokenError
from src.schemas.jwt import DeleteRefresh


def create_token_by_email(req: Create, db: Session):
    user = db.query(User).filter(User.email == req.email).first()

    if user is None:
        raise NotUserExistException()

    if pwd.check_password(user.salt + req.password, user.hashedpass) is False:
        raise PasswordNotMatchError()

    access_token = jwt.create_access_token(user.email)

    refresh_token = jwt.create_refresh_token(user.id, db)

    return {"access_token": access_token, "refresh_token": refresh_token}


def token_republish_by_refresh_token(req: RefreshSchema, db: Session):
    decoded = jwt.decoded_refresh_token(req.refresh_token)

    if int(datetime.utcnow().timestamp()) > decoded.exp:
        raise ExpiredSignatureError()

    valid_refresh = db.query(Refresh).filter(Refresh.id == decoded.sub)

    if valid_refresh.first() is None:
        raise InvalidTokenError()

    if valid_refresh.filter(Refresh.kid == decoded.kid).first() is None:
        raise InvalidTokenError()

    user = db.query(User).filter(User.id == decoded.sub).first()

    access_token = jwt.create_access_token(user.email)

    refresh_token = jwt.create_refresh_token(user.id, db)

    return {"access_token": access_token, "refresh_token": refresh_token}


def delete_refresh_token_by_email(req: DeleteRefresh, db: Session):
    user = db.query(User).filter(User.email == req.email).first()

    if user is None:
        raise NotUserExistException()

    valid_refresh = db.query(Refresh).filter(Refresh.id == user.id)

    if valid_refresh.first() is None:
        raise InvalidTokenError()

    valid_refresh.delete()
    db.commit()

    return
