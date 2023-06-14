from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.cruds import users
from src.db.database import get_db
from src.utils.exeption import AlreadyExistUserError, NotUserExistException
from src.schemas.user import Read, Create
from fastapi import HTTPException
from src.libs import pwd

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/{id}", response_model=Read)
def get_one_user(id: int, db: Session = Depends(get_db), _=Depends(pwd.get_cuurent_user)):
    try:
        return users.get_one_member(id, db)
    except NotUserExistException:
        raise HTTPException(404, f"Not Found id = {id}")


@router.post("/", response_model=Read)
def create_user(request: Create, db: Session = Depends(get_db)):
    try:
        return users.create_user(request, db)
    except AlreadyExistUserError:
        raise HTTPException(409, f"{request.email} is already exist")
