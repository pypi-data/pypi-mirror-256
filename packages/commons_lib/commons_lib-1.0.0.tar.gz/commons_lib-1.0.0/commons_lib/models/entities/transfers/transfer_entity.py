from datetime import date
from typing import Optional
from sqlalchemy import Column, BIGINT, DateTime
from sqlalchemy.orm import Mapped

from server_main.models.entities.base_entity import BaseEntity


class TransferEntity(BaseEntity):
    __tablename__ = "transfers"
    from_appreciation_account: Mapped[Optional[int]] = Column(BIGINT,nullable=True)
    to_appreciation_account: Mapped[Optional[int]] = Column(BIGINT,nullable=True)
    from_personal_account: Mapped[Optional[int]] = Column(BIGINT,nullable=True)
    to_personal_account: Mapped[Optional[int]] = Column(BIGINT,nullable=True)
    expire_at: Mapped[date] = Column(DateTime,nullable=False)
