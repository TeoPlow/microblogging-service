from sqlalchemy import (
    Column,
    BigInteger,
    Text,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship
from app.api.database import Base


class Tweet(Base):
    """
    Модель твита.
    """
    __tablename__ = "tweets"

    id = Column(BigInteger, primary_key=True)
    content = Column(Text, nullable=False)
    author_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="tweets")
    attachments = relationship(
        "Attachment", back_populates="tweet", cascade="all, delete-orphan"
    )
    medias = relationship(
        "Media",
        back_populates="tweet",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    likes = relationship(
        "Like", back_populates="tweet", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("idx_tweets_author_id", "author_id"),)
