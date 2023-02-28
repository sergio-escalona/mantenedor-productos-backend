from datetime import date, datetime
from typing import Optional, List, Literal, Any
from pydantic import BaseModel, Field


class GetPaginated(BaseModel):
    filters: dict
    table_filters: dict
    joinModel: Any
    joins: List[Any]
    options: List[Any]
    pag_params: Any
    db: Any
    order: str
