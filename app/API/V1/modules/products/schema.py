from pydantic import BaseModel, Field
from ..product_categories.schema import ProductCategoryBase


class ProductBase(BaseModel):
    name: str
    short_name: str = Field(..., alias="shortName")
    description: str
    price: int
    category_id: int = Field(..., alias="categoryId")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Fruto seco",
                "short_name": "Fruto seco",
                "description": "Fruto seco",
                "price": 1000,
                "category_id": 1,
            }
        }


class ProductCreate(ProductBase):
    pass


class ProductItem(ProductBase):
    code: int
    product_categories: ProductCategoryBase
