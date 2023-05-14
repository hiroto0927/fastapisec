from sqlalchemy import Column, Integer, String

from src.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column("id",Integer, primary_key=True,autoincrement=True)
    name = Column("name",String(20),nullable=False)
    salt = Column("salt",String,nullable=False)
    hashedpass = Column("hashedpass",String,nullable=False)

    class Config:
        orm_mode = True