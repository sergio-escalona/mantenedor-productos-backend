from typing import List
from fastapi import APIRouter, Query
from fastapi.param_functions import Depends
from sqlalchemy import func
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import and_
from starlette.responses import StreamingResponse
from io import BytesIO
import xlsxwriter
from app.database.main import get_database
from ...services.CRUD import CrudService
from ..products.model import Product
from ..product_categories.model import ProductCategory

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

dash_service = CrudService(Model=Product)


@router.get("/graphs")
def get_graphs(
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


def products_to_xlsx(data):
    try:
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        title = workbook.add_format({"bold": True})
        worksheet = workbook.add_worksheet("Productos")
        worksheet.set_column(0, 1, 10)
        worksheet.set_column(2, 3, 15)
        worksheet.write("A1", "Categoría", title)
        worksheet.write("B1", "Id", title)
        worksheet.write("C1", "Total stock", title)
        worksheet.write("D1", "Cant. productos", title)

        row = 1
        col = 0

        for product in data:
            worksheet.write(row, col, product["name"])
            worksheet.write(row, col + 1, product["category_id"])
            worksheet.write(row, col + 2, product["total"])
            worksheet.write(row, col + 3, product["count"])

            row += 1

        workbook.close()
        output.seek(0)

        return output

    except Exception as err:
        print("Error message : {0}".format(err))


@router.post("/xlsx")
def get_xlsx(
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
            Product.category_id.label("category_id"),
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
    xlsx = products_to_xlsx(products)
    headers = {"Content-Disposition": "attachment; filename=productos.xlsx"}

    return StreamingResponse(xlsx, headers=headers)
