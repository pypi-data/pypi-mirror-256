from sqlmodel import VARCHAR, Integer
from sqlalchemy import Column, BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from server_main.models.entities.base_entity import BaseEntity


class WinningEntity(BaseEntity):
    __tablename__ = "Winnings"

    title: Mapped[str] = Column(VARCHAR(255), nullable=False)
    description: Mapped[str] = Column(VARCHAR(1000))
    price: Mapped[int] = Column(Integer, nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("company.pk_uuid"))
