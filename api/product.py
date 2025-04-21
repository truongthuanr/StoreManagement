from fastapi import APIRouter, Depends, Request
# from fastapi.responses import JSONRespons
from sqlalchemy.orm import Session

# from model.request.buyer import BuyerReq, PurchaseHistoryReq, PurchaseStatusReq
from repository.product import ProductRepository
# from db_config.pymongo_config import create_db_collections
from db_config.mysql_config import SessionFactory

from datetime import date, datetime
from json import dumps, loads
from bson import ObjectId

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.get("/products")
def list_products(request: Request, db: Session = Depends(sess_db)):
    repo = ProductRepository(db)
    products = repo.get_all()
    print(products)
    return templates.TemplateResponse("product/list.html", {
        "request": request,
        "products": products
    })