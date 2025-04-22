from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from model.data.models import Product, User  # SQLAlchemy Product model
from db_config.mysql_config import sess_db
from auth.dependencies import require_admin
from fastapi.templating import Jinja2Templates
from utils.template import render_template



router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin", response_class=HTMLResponse)
def admin_home(request: Request, admin: User = Depends(require_admin)):
    return templates.TemplateResponse("admin/admin.html", {
        "request": request,
        "admin": admin
    })


@router.get("/admin/products", response_class=HTMLResponse)
def admin_products(request: Request, db: Session = Depends(sess_db), admin: User = Depends(require_admin)):
    products = db.query(Product).all()
    return templates.TemplateResponse("admin/product.html", {
        "request": request,
        "products": products,
        "admin": admin
    })


@router.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(sess_db), admin: User = Depends(require_admin)):
    total_users = db.query(User).count()
    total_products = db.query(Product).count()
    total_orders = 99 #db.query(Order).count()
    total_revenue = 99  # db.query(func.sum(Payment.amount)).scalar() or 0  # assuming "amount" column

    return render_template(request, "admin/dashboard.html", {
        "request": request,
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "admin": admin
    })