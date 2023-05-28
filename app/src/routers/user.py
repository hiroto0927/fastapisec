from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.cruds import users
from src.db.database import get_db
from src.utils.exeption import NotFoundException
from src.schemas.user import Read, Create
from fastapi import HTTPException
from src.libs import token
from src.libs import token

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/{id}", response_model=Read)
def get_one_user(
    id: int, db: Session = Depends(get_db), _=Depends(token.get_cuurent_user)
):
    try:
        return users.get_one_member(id, db)
    except NotFoundException:
        raise HTTPException(404, f"Not Found id = {id}")


@router.post("/", response_model=Read)
def create_user(request: Create, db: Session = Depends(get_db)):
    return users.create_user(request, db)
