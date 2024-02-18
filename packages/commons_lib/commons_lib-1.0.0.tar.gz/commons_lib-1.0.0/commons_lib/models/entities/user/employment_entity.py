from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Column, BIGINT
from sqlalchemy import VARCHAR
from sqlalchemy.dialects.postgresql import UUID


from server_main.models.entities.base_entity import BaseEntity


class EmploymentEntity(BaseEntity):
    __tablename__ = "employment"

    employee_id: UUID = Column(UUID(as_uuid=True), ForeignKey('employees.pk_uuid'))
    employee = relationship(argument='EmployeeEntity', back_populates="employments")
    profile = Column(VARCHAR(1000), nullable=True)
    org_email = Column(VARCHAR(320), nullable=True, unique=True)
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.pk_uuid"), nullable=True)
    position = relationship("Position", back_populates="employees")  # Adjust the attribute name here
    accounts = relationship(argument='AccountEntity', back_populates="employee")
    redeems = relationship(argument='RedeemEntity', back_populates='employee')
    transactions = relationship(argument='TransactionEntity', back_populates='employee')
    organization_id = Column(UUID(as_uuid=True), ForeignKey("company.pk_uuid"))

    sent_appreciations = relationship("AppreciationEntity", back_populates="from_employment", foreign_keys="AppreciationEntity.from_employment_id")
    received_appreciations = relationship("AppreciationEntity", back_populates="to_employment", foreign_keys="AppreciationEntity.to_employment_id")
