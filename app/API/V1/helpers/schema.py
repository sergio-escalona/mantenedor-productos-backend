from datetime import date, datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class SuccessMessage(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Item eliminado",

            }
        }
