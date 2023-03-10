from pydantic import BaseModel


class SuccessMessage(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Item eliminado",
            }
        }
