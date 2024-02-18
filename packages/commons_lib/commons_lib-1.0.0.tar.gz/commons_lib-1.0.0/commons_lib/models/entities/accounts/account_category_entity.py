from sqlalchemy import VARCHAR, Column
from sqlalchemy.orm import relationship

from server_main.models.entities.base_entity import BaseEntity


class AccountCategoryEntity(BaseEntity):

    __tablename__ = "accounts_type"

    title: str = Column(VARCHAR(256), nullable=False)
    slug: str = Column(VARCHAR(512), nullable=False)
    accounts = relationship(argument='AccountEntity', back_populates="account_type")

