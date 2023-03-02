from typing import List
from fastapi import APIRouter, Query, Request
from fastapi.param_functions import Depends
from sqlalchemy import func
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import or_, and_
from fastapi_pagination import Params, Page
from app.database.main import get_database
from ...services.CRUD import CrudService
from ...helpers.schema import SuccessMessage
from ..products.model import Product
from ..product_categories.model import ProductCategory

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

dash_service = CrudService(Model=Product)


@router.get("/graphs")
def get_all(
    start_date: str = Query(None, alias="startDate"),
    end_date: str = Query(None, alias="endDate"),
    db: Session = Depends(get_database),
):
    start_filter = []
    end_filter = []

    if start_date:
        start_filter.append(Product.created_at >= start_date)

    if end_date:
        end_date = end_date + " 23:59:59"
        end_filter.append(Product.created_at <= end_date)

    products = (
        db.query(
            Product.category_id.label("categoryId"),
            ProductCategory.name,
            func.sum(Product.stock).label("total"),
            func.count(Product.stock).label("count"),
        )
        .join(ProductCategory)
        .filter(
            Product.is_deleted == False,
            and_(*start_filter),
            and_(*end_filter),
        )
        .group_by(Product.category_id, ProductCategory.name)
        .all()
    )

    return products
