from sqlalchemy.orm import Session
from src.models.user import User
from src.utils.exeption import NotFoundException
from src.schemas.user import Create
from src.libs import hashed

def get_one_member(id:int,db:Session):

    if db.query(User).filter(User.id == id).first() == None:
        raise NotFoundException()

    return db.query(User).filter(User.id == id).first()

def create_user(user:Create,db:Session):

    rand = hashed.randomstr(10)
    hash = hashed.get_password_hashed(user.password,rand)

    query = User(name=user.name, salt = rand, hashedpass = hash)
    db.add(query)
    db.commit()

    return query