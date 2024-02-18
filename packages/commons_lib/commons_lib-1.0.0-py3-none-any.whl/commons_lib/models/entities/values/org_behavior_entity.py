from sqlalchemy import Column, VARCHAR, Table, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID

from server_main.models.entities.base_entity import BaseEntity, Base


class OrgBehaviorEntity(BaseEntity):
        __tablename__ = "organizationBehaviors"

        title: Mapped[str] = Column(VARCHAR(255))
        description: Mapped[str] = Column(VARCHAR(1000))

        values = relationship("OrgValueEntity", secondary="orgValueBehavior", back_populates="behaviors")
        appreciations = relationship("AppreciationEntity", secondary="appreciationBehavior", back_populates="behaviors")


org_value_behavior = Table(
    "orgValueBehavior",
    Base.metadata,
    Column("org_value_pk_uuid", UUID(as_uuid=True), ForeignKey("organizationValues.pk_uuid"), primary_key=True),
    Column("org_behavior_pk_uuid", UUID(as_uuid=True), ForeignKey("organizationBehaviors.pk_uuid"), primary_key=True),
)
