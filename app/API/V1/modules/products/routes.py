from typing import List
from fastapi import APIRouter, Query, Request
from fastapi.param_functions import Depends
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import or_, and_
from fastapi_pagination import Params, Page
from app.database.main import get_database
from ...services.CRUD import CrudService
from ...helpers.schema import SuccessMessage
from .schema import ProductCreate, ProductItem
from .model import Product
from ..product_categories.model import ProductCategory

router = APIRouter(prefix="/products",
                   tags=["Products"])

product_service = CrudService(Model=Product)


@router.get("/all", response_model=List[ProductItem])
def get_all(db: Session = Depends(get_database)):
    return product_service.find_all(db)


@router.get("", response_model=Page[ProductItem])
def get_list(name: str = None,
             short_name: str = Query(None, alias="shortName"),
             description: str = None,
             price: int = None,
             category_id: int = Query(None, alias="categoryId"),
             sort: str = None,
             db: Session = Depends(get_database),
             pag_params: Params = Depends()):
    table_filters = [
        {"col_name": "name", "value": name, "type": "str"},
        {"col_name": "short_name", "value": short_name, "type": "str"},
        {"col_name": "description", "value": description, "type": "str"},
        {"col_name": "price", "value": price, "type": "int"},
        {"col_name": "category_id", "value": category_id, "type": "int"},
        ]
    joins = [(ProductCategory, and_(
        ProductCategory.id == Product.category_id)),
        ]
    options = [contains_eager("product_categories")]
    return product_service.find_paginated({"joinModel": ProductCategory,
                                           "joins": joins,
                                           "options": options,
                                           'filters':[],
                                           "table_filters": table_filters,
                                           "pag_params": pag_params,
                                           "db": db,
                                           "sort": sort})


@router.post("", response_model=ProductItem)
def create(request: Request,
           body: ProductCreate,
           db: Session = Depends(get_database)):
    return product_service.create(body, db)


@ router.get("/{code}", response_model=ProductItem)
def get_by_code(code: int,
                db: Session = Depends(get_database)):
    return product_service.find_one(code, db)


@ router.put("/{code}", response_model=ProductItem)
def updated_by_code(code: int,
                    update_body: ProductCreate,
                    db: Session = Depends(get_database)):
    return product_service.update_one(code, update_body, db)


@ router.delete("/{code}", response_model=SuccessMessage)
def delete_by_code(code: int,
                   db: Session = Depends(get_database)):
    return product_service.delete_one(code,  db)
