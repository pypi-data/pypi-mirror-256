from sqlalchemy import BIGINT, Column
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID


from server_main.models.entities.base_entity import BaseEntity


class RedeemEntity(BaseEntity):
    __tablename__ = "redeems"
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employment.pk_uuid"))
    employee = relationship('EmploymentEntity', back_populates='redeems')
