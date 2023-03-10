from typing import List
from fastapi import APIRouter, Query, Request
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from fastapi_pagination import Params, Page
from app.database.main import get_database
from ...helpers.security import get_password_hash
from ...helpers.mailer import send_welcome_mail
from ...services.CRUD import CrudService
from ...helpers.schema import SuccessMessage
from .schema import UserCreate, UserItem
from .model import User

router = APIRouter(prefix="/users", tags=["Users"])

user_service = CrudService(Model=User)


@router.get("/all", response_model=List[UserItem])
def get_all(db: Session = Depends(get_database)):
    return user_service.find_all(db)


@router.get("", response_model=Page[UserItem])
def get_list(
    first_name: str = Query(None, alias="firstName"),
    last_name: str = Query(None, alias="lastName"),
    email: str = None,
    sort: str = None,
    db: Session = Depends(get_database),
    pag_params: Params = Depends(),
):
    table_filters = [
        {"col_name": "first_name", "value": first_name, "type": "str"},
        {"col_name": "last_name", "value": last_name, "type": "str"},
        {"col_name": "email", "value": email, "type": "str"},
    ]
    return user_service.find_paginated(
        {
            "filters": [],
            "table_filters": table_filters,
            "pag_params": pag_params,
            "db": db,
            "sort": sort,
        }
    )


@router.post("", response_model=UserItem)
def create(request: Request, body: UserCreate, db: Session = Depends(get_database)):
    send_welcome_mail(body.email, body.first_name, body.password)
    body.password = (get_password_hash(body.password),)
    return user_service.create(body, db)


@router.get("/{id}", response_model=UserItem)
def get_by_code(id: int, db: Session = Depends(get_database)):
    return user_service.find_one(id, db)


@router.put("/{id}", response_model=UserItem)
def updated_by_code(
    id: int, update_body: UserCreate, db: Session = Depends(get_database)
):
    update_body.password = (get_password_hash(update_body.password),)
    return user_service.update_one(id, update_body, db)


@router.delete("/{id}", response_model=SuccessMessage)
def delete_by_code(id: int, db: Session = Depends(get_database)):
    return user_service.delete_one(id, db)
