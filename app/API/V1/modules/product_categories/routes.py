from typing import List
from fastapi import APIRouter, Request
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from fastapi_pagination import Params, Page
from app.database.main import get_database
from ...services.CRUD import CrudService
from ...helpers.schema import SuccessMessage
from .schema import ProductCategoryCreate, ProductCategoryItem
from .model import ProductCategory

router = APIRouter(prefix="/products-category", tags=["ProductCategories"])

product_category_service = CrudService(Model=ProductCategory)


@router.get("/all", response_model=List[ProductCategoryItem])
def get_all(db: Session = Depends(get_database)):
    return product_category_service.find_all(db)


@router.get("", response_model=Page[ProductCategoryItem])
def get_list(
    name: str = None,
    sort: str = None,
    db: Session = Depends(get_database),
    pag_params: Params = Depends(),
):
    table_filters = [{"col_name": "name", "value": name, "type": "str"}]
    return product_category_service.find_paginated(
        {
            "filters": [],
            "table_filters": table_filters,
            "pag_params": pag_params,
            "db": db,
            "sort": sort,
        }
    )


@router.post("", response_model=ProductCategoryItem)
def create(
    request: Request, body: ProductCategoryCreate, db: Session = Depends(get_database)
):
    return product_category_service.create(body, db)


@router.get("/{code}", response_model=ProductCategoryItem)
def get_by_code(code: int, db: Session = Depends(get_database)):
    return product_category_service.find_one(code, db)


@router.put("/{code}", response_model=ProductCategoryItem)
def updated_by_code(
    code: int, update_body: ProductCategoryCreate, db: Session = Depends(get_database)
):
    return product_category_service.update_one(code, update_body, db)


@router.delete("/{code}", response_model=SuccessMessage)
def delete_by_code(code: int, db: Session = Depends(get_database)):
    return product_category_service.delete_one(code, db)
