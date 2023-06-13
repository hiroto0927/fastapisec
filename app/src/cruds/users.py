from sqlalchemy.orm import Session
from src.models.user import User
from src.utils.exeption import AlreadyExistUserError, NotUserExistException
from src.schemas.user import Create
from src.libs import pwd


def get_one_member(id: int, db: Session):
    if db.query(User).filter(User.id == id).first() == None:
        raise NotUserExistException()

    return db.query(User).filter(User.id == id).first()


def create_user(user: Create, db: Session):
    rand = pwd.randomstr(10)
    hash = pwd.get_password_hashed(user.password, rand)

    exist_user = db.query(User).filter(User.email == user.email).first()
    if exist_user is not None:
        raise AlreadyExistUserError()

    new_user = User(name=user.name, salt=rand, hashedpass=hash, email=user.email)
    db.add(new_user)
    db.commit()

    return new_user
