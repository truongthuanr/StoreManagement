from typing import Dict, Any
from dataclasses import asdict
from sqlalchemy.orm import Session
from model.data.models import Product

from datetime import date, datetime
from bson.json_util import dumps
import json
from bson.dbref import DBRef


class ProductRepository:
    def __init__(self, sess: Session):
        self.sess: Session = sess

    def get_all(self, skip: int = 0, limit: int = 100):
        # return self.sess.query(Product).offset(skip).limit(limit).all()
        return self.sess.query(Product).all()


    def get_by_id(self, product_id: int):
        return self.sess.query(Product).filter(Product.id == product_id).one_or_none()

    def get_by_category(self, category_id: int):
        return self.sess.query(Product).filter(Product.category_id == category_id).all()

    def create(self, product: Product) -> bool:
        try:
            self.sess.add(product)
            self.sess.commit()
            self.sess.refresh(product)
        except:
            return False
        return True
    

    def update(self, product_id: int, updates: dict) -> bool:
        db_product = self.get_by_id(product_id)
        if not db_product:
            return None
        for key, value in updates.items():
            setattr(db_product, key, value)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete(self, product_id: int) -> bool:
        db_product = self.get_by_id(product_id)
        if not db_product:
            return False
        self.db.delete(db_product)
        self.db.commit()
        return True