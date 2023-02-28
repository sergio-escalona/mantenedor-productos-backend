from typing import Optional, List
from pydantic import BaseModel, Field

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "correo@mail.com",
                "password": "HolaHola22..",
            }
        }


class MeResponseSchema(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    accessToken: str
    refreshToken: str
    user: MeResponseSchema
