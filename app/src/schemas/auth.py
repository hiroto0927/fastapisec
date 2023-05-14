from pydantic import BaseModel,Field,EmailStr

class Read(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

class Create(BaseModel):
    password: str = Field(min_length=8,max_length=20)
    email:EmailStr