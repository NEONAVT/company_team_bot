from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, BigInteger, String, ForeignKey
from database.database import Base
from settings import settings
from typing import Optional
from menu.models import Recipes

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default=settings.GUEST_ROLE)
    access_key: Mapped[Optional[str]] = mapped_column(String, default=None)

    recipes = relationship("Recipes", back_populates="author")
    admin = relationship("Admins", back_populates="user", uselist=False)


class Admins(Base):
    __tablename__ = "admins"

    admin_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String)

    user = relationship("User", back_populates="admin")






