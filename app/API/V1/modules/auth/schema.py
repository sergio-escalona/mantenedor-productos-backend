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


class ForgotSchema(BaseModel):
    email: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "correo@mail.com",
            }
        }


class RecoverSchema(BaseModel):
    token: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "correo@mail.com",
            }
        }


class ChangeSchema(BaseModel):
    id: str
    old_pass: str = Field(..., alias="oldPass")
    new_pass: str = Field(..., alias="newPass")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "correo@mail.com",
            }
        }


class MeResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    accessToken: str
    refreshToken: str
    user: MeResponseSchema
