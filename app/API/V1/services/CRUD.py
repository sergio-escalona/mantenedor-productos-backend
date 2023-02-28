from typing import List, Literal
from sqlalchemy.orm.session import Session
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy.sql.expression import or_, and_
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from app.database.base_class import Base
from .schema import GetPaginated


class CrudService:

    def __init__(self, Model: Base) -> None:
        self.Model = Model

    """
    Find all active rows 
    """

    def find_all(self, db: Session):
        return db.query(self.Model).filter(self.Model.is_deleted == False).all()

    """
    Format filter
    """

    def format_filter(self, col_name: str, filter_type: str, filter_value):
        switch = {
            "str": self.Model.__getattribute__(self.Model, col_name).ilike("{}%".format(filter_value)),
            "bool": self.Model.__getattribute__(self.Model, col_name) == filter_value,
            "int": self.Model.__getattribute__(self.Model, col_name) == filter_value
        }

        return switch.get(filter_type, None)

    """
    Get filters 
    """

    def get_filters(self, filters_list: List[dict]):
        generated_filters = []
        for item in filters_list:

            if hasattr(self.Model, item["col_name"]) and item["value"] != None:
                generated_filters.append(self.format_filter(
                    item["col_name"], item["type"], item["value"]))

        return generated_filters
    """
    Get order option
    """

    def get_order_option(self, order: Literal["asc", "desc"] = None):
        switch = {
            "asc": self.Model.created_at.asc(),
            "desc": self.Model.created_at.desc(),
        }

        return switch.get(order, self.Model.created_at.desc())

    """
    Find rows filtering and paginating 
    """

    def find_paginated(self, body: GetPaginated):
        filters_list = self.get_filters(body["filters"])
        table_filters_list = self.get_filters(body["table_filters"])

        query = body["db"].query(self.Model)

        if hasattr(body, "joins") and body["joins"] != None:

            for q_join in body["joins"]:
                query = query.outerjoin(q_join)
        if hasattr(body, "options") and body["options"] != None:
            query = query.options(*body["options"])

        query = query.order_by(self.get_order_option(body["sort"]))
        query = query.filter(and_(and_(or_(*filters_list), and_(*table_filters_list)),
                                  self.Model.is_deleted == False))

        return paginate(query, body["pag_params"])
    """
    Find row by id or code 
    """

    def find_one(self, id: int, db: Session):

        found_item = None

        if hasattr(self.Model, "id"):
            found_item = db.query(self.Model).filter(
                self.Model.id == id).first()
        else:
            found_item = db.query(self.Model).filter(
                self.Model.code == id).first()

        if not found_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Item no encontrado")
        return found_item

    """
    Find by name
    """

    def find_by_name(self, name: str, db: Session):
        if not hasattr(self.Model, "name"):
            return None

        item = db.query(self.Model).filter(
            and_(self.Model.name == name, self.Model.is_deleted == False)).first()

        return item

    """
    Create new row 
    """

    def create(self, body: dict, db: Session):
        encoded_item = jsonable_encoder(body, by_alias=False)

        if hasattr(body, "name"):
            item_by_name = self.find_by_name(body.name, db)

            if item_by_name:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Nombre %s ya esta registrado" % (body.name))

        new_item = self.Model(**encoded_item)

        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return new_item

    """
    Create sub items in a one-to-many relation
    """

    def create_sub_item(self, SubModel: Base, parent_id: int, parent_col_name: str, items: List[dict], db: Session):
        for sub_item in items:
            encoded_sub_item = jsonable_encoder(sub_item, by_alias=False)
            encoded_sub_item[parent_col_name] = parent_id

            db_sub_item = SubModel(**encoded_sub_item)

            db.add(db_sub_item)
            db.commit()
            db.refresh(db_sub_item)

    """
    Update by id or code 
    """

    def update_one(self, id: int, body: dict, db: Session):

        found_item = self.find_one(id, db)

        updated_item = self.get_updated_row(found_item, body)

        db.add(updated_item)
        db.commit()
        db.refresh(updated_item)

        return updated_item

    """
    Delete by id or code 
    """

    def delete_one(self, id: int, db: Session):

        found_item = self.find_one(id, db)

        if found_item.is_deleted:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Item ya fue eliminado")

        found_item.is_deleted = True

        db.add(found_item)
        db.commit()
        db.refresh(found_item)

        return {"message": 'Item eliminado'}

    """
    Update a db object with update body from request
    """

    def get_updated_row(self, db_obj, update_body):
        obj_data = jsonable_encoder(db_obj)

        if isinstance(update_body, dict):
            update_data = update_body
        else:
            update_data = update_body.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        return db_obj
