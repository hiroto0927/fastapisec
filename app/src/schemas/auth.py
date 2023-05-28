from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class Read(BaseModel):
    access_token: str
    # token_type: str

    class Config:
        orm_mode = True


class Create(BaseModel):
    password: str = Field(min_length=8, max_length=20)
    email: EmailStr


class AuthUser(Create):
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


class PublicKey(BaseModel):
    kty:str
    n: str
    e:str

    class Config:
        orm_mode = True


class Refresh(BaseModel):
    refresh_token: str

    class Config:
        orm_mode = True


class RefreshDecoded(BaseModel):
    sub: int
    kid: str
    iat: int
    exp: int

    class Config:
        orm_mode = True
