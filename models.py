from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        Text,
        nullable=False
    )

    description = Column(
        Text
    )

    measurements = Column(
        Text
    )