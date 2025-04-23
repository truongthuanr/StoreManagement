from sqlalchemy.orm import Session
from model.data.models import Product  # Đảm bảo bạn đã import đúng model

class ProductRepository:
    def __init__(self, sess: Session):
        self.sess = sess

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.sess.query(Product).offset(skip).limit(limit).all()

    def get_by_id(self, product_id: int):
        return self.sess.query(Product).filter(Product.id == product_id).one_or_none()

    def get_by_category(self, category_id: int):
        return self.sess.query(Product).filter(Product.category_id == category_id).all()

    def create(self, product: Product) -> bool:
        try:
            self.sess.add(product)
            self.sess.commit()
            self.sess.refresh(product)
            return True
        except Exception as e:
            self.sess.rollback()
            print("Error creating product:", e)
            return False

    def update(self, product_id: int, updates: dict):
        db_product = self.get_by_id(product_id)
        if not db_product:
            return None
        for key, value in updates.items():
            setattr(db_product, key, value)
        try:
            self.sess.commit()
            self.sess.refresh(db_product)
            return db_product
        except Exception as e:
            self.sess.rollback()
            print("Error updating product:", e)
            return None

    def delete(self, product_id: int) -> bool:
        db_product = self.get_by_id(product_id)
        if not db_product:
            return False
        try:
            self.sess.delete(db_product)
            self.sess.commit()
            return True
        except Exception as e:
            self.sess.rollback()
            print("Error deleting product:", e)
            return False
