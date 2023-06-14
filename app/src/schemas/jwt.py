from pydantic import BaseModel, EmailStr


class RefreshDecoded(BaseModel):
    sub: int
    kid: str
    iat: int
    exp: int

    class Config:
        orm_mode = True


class PublicKey(BaseModel):
    kty: str
    n: str
    e: str

    class Config:
        orm_mode = True


class Refresh(BaseModel):
    refresh_token: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str


class DeleteRefresh(BaseModel):
    email: EmailStr


class DeleteResponse(BaseModel):
    message: str
