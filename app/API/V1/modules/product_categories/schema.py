from pydantic import BaseModel, Field


class ProductCategoryBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Fruto seco",
            }
        }


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryItem(ProductCategoryBase):
    id: int
