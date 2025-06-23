from sqlalchemy import (
    Column,
    BigInteger,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.api.database import Base


class Attachment(Base):
    __tablename__ = "attachments"
    tweet_id = Column(BigInteger, ForeignKey("tweets.id"), primary_key=True)
    link = Column(Text, primary_key=True)

    tweet = relationship("Tweet", back_populates="attachments")
