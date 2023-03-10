from sqlalchemy import Column, Integer, String
from app.database.base_class import Base, TimestampMixin, UserOperations, DeletedMixin


class User(Base, DeletedMixin, UserOperations, TimestampMixin):
    """
    User
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(500), nullable=False)
