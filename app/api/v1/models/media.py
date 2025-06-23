from sqlalchemy import (
    Column,
    BigInteger,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.api.database import Base


class Media(Base):
    __tablename__ = "medias"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tweet_id = Column(BigInteger, ForeignKey("tweets.id"), nullable=True)
    filename = Column(Text, nullable=False)

    tweet = relationship("Tweet", back_populates="medias")
