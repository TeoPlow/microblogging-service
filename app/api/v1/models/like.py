from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship
from app.api.database import Base


class Like(Base):
    __tablename__ = "likes"
    tweet_id = Column(BigInteger, ForeignKey("tweets.id"), primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)

    tweet = relationship("Tweet", back_populates="likes")
    user = relationship("User", back_populates="likes")

    __table_args__ = (Index("idx_likes_user_id", "user_id"),)
