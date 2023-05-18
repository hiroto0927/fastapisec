from sqlalchemy import Column, Integer, String, ForeignKey
from src.db.database import Base


class Refresh(Base):
    __tablename__ = "refresh_token"

    id = Column(
        "id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        autoincrement=True,
    )
    salt = Column("salt", String, nullable=False)
    refresh = Column("refresh", String, nullable=False)
