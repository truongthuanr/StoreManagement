from fastapi import APIRouter, Depends, Form, Request, HTTPException 
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from model.data.models import Cart, CartItem, Product, Category
from auth.dependencies import get_current_user
from db_config.mysql_config import sess_db
from utils.template import render_template

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def homepage(request: Request, db: Session = Depends(sess_db)):
    print("call home page")
    categories = db.query(Category).all()
    featured_products = db.query(Product).order_by(Product.created_at.desc()).limit(8).all()
    return render_template(request, "home.html", {
        "request": request,
        "categories": categories,
        "featured_products": featured_products
    })