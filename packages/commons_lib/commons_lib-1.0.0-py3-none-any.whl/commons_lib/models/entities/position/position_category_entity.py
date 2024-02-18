from typing import List

from sqlalchemy import String, Column
from sqlalchemy.orm import relationship, Mapped

from server_main.models.entities.base_entity import BaseEntity


class PositionCategoryEntity(BaseEntity):
    __tablename__ = "positionTypes"

    positions = relationship('Position',back_populates="positionType")
    positionTypeName: Mapped[str] = Column(String(255),nullable=False)
    description: Mapped[str] = Column(String(1000))


    