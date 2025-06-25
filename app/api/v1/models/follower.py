from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship
from app.api.database import Base


class Follower(Base):
    """
    Модель подписки.
    """
    __tablename__ = "followers"
    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    follower_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)

    user = relationship(
        "User", foreign_keys=[user_id], back_populates="followers_rel"
    )
    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="following_rel"
    )

    __table_args__ = (Index("idx_followers_follower_id", "follower_id"),)
