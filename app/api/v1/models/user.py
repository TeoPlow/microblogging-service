from sqlalchemy import (
    Column,
    BigInteger,
    Text,
)
from sqlalchemy.orm import relationship
from app.api.database import Base


class User(Base):
    """
    Модель пользователя.
    Содержит информацию о пользователе и его взаимодействиях.
    """
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)

    tweets = relationship(
        "Tweet", back_populates="author", cascade="all, delete-orphan"
    )
    likes = relationship(
        "Like", back_populates="user", cascade="all, delete-orphan"
    )
    following_rel = relationship(
        "Follower",
        foreign_keys="Follower.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan",
    )
    followers_rel = relationship(
        "Follower",
        foreign_keys="Follower.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @property
    def followers(self) -> list["User"]:
        return [f.follower for f in self.followers_rel]

    @property
    def following(self) -> list["User"]:
        return [f.user for f in self.following_rel]
