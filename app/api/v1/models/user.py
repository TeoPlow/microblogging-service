from sqlalchemy import (
    Column,
    BigInteger,
    Text,
)
from sqlalchemy.orm import relationship
from app.api.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)

    tweets = relationship(
        "Tweet", back_populates="author", cascade="all, delete-orphan"
    )
    likes = relationship(
        "Like", back_populates="user", cascade="all, delete-orphan"
    )
    following = relationship(
        "Follower",
        foreign_keys="Follower.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan",
    )
    followers = relationship(
        "Follower",
        foreign_keys="Follower.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @property
    def followers_users(self) -> list["User"]:
        return [f.follower for f in self.followers]

    @property
    def following_users(self) -> list["User"]:
        return [f.user for f in self.following]
