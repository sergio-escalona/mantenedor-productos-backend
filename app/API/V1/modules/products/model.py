from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from app.database.base_class import Base, TimestampMixin, UserOperations, DeletedMixin


class Product(Base, DeletedMixin, UserOperations, TimestampMixin):
    """
    Product
    """
    __tablename__ = "products"
    code = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    short_name = Column(String(50), nullable=False)
    description = Column(String(1000), nullable=False)
    price  = Column(Integer, nullable=False)
    category_id = Column(
        Integer, ForeignKey("product_categories.id"), nullable=False, server_default="1"
    )

    product_categories = relationship("ProductCategory", back_populates="products", lazy="joined")
