from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base_class import Base, TimestampMixin, UserOperations, DeletedMixin


class ProductCategory(Base, DeletedMixin, UserOperations, TimestampMixin):
    """
    ProductCategory
    """

    __tablename__ = "product_categories"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    products = relationship("Product", back_populates="product_categories")
