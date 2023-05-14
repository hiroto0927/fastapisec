from pydantic import BaseModel,Field

class Read(BaseModel):
    id:int
    name:str

    class Config:
        orm_mode = True

class Create(BaseModel):
    name:str = Field(min_length=1,max_length=20)
    password: str = Field(min_length=8,max_length=20)