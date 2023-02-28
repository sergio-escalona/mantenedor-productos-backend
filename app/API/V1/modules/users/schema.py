from pydantic import BaseModel, Field


class UserBase(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    email: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "first_name": "Sergio",
                "last_name": "Escalona",
                "email": "correo@mail.com",
            }
        }


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "first_name": "Sergio",
                "last_name": "Escalona",
                "email": "correo@mail.com",
                "password": "HolaHola22..",
            }
        }


class UserItem(UserBase):
    id: int
