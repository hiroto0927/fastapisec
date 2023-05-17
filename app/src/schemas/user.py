from pydantic import BaseModel, Field, EmailStr


class Read(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class Create(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    password: str = Field(min_length=8, max_length=20)
    email: EmailStr
