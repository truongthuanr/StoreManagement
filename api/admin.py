from fastapi import APIRouter, Depends, Request, HTTPException, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from typing import Optional
import os, shutil
from uuid import uuid4


from config.config import *
from utils.template import render_template
from model.data.models import Category, Product, User  # SQLAlchemy Product model
from db_config.mysql_config import sess_db
from auth.dependencies import require_admin




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
        "admin": admin,
        "upload_dir": UPLOAD_DIR,
    })

@router.get("/admin/products/{product_id}/edit", response_class=HTMLResponse)
def edit_product_form(product_id: int, request: Request, db: Session = Depends(sess_db), user=Depends(require_admin)):
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")

    categories = db.query(Category).all()

    return render_template(request, "admin/product_edit.html", {
        "product": product,
        "categories": categories,
        "user": user
    })

@router.post("/admin/products/{product_id}/edit", response_class=HTMLResponse)
def update_product(
    product_id: int,
    request: Request,
    name: str = Form(...),
    price: float = Form(...),
    description: str = Form(""),
    category_id: int = Form(...),
    db: Session = Depends(sess_db),
    user=Depends(require_admin)
):
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")

    product.name = name
    product.price = price
    product.description = description
    product.category_id = category_id
    db.commit()

    # Redirect về trang danh sách sản phẩm hoặc thông báo cập nhật thành công
    return RedirectResponse(url="/admin/products", status_code=303)


@router.get("/admin/products/add")
def show_create_form(request: Request, db: Session = Depends(sess_db)):
    categories = db.query(Category).all()
    return templates.TemplateResponse("admin/product_add.html", {"request": request, "categories": categories})

@router.post("/admin/products/add")
def create_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    stock: int = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(sess_db),
):
    # Tạo file name ngẫu nhiên
    ext = image.filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # Lưu file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Tạo bản ghi mới
    new_product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category_id,
        image_url=filename,
    )
    db.add(new_product)
    db.commit()

    return RedirectResponse("/admin/products", status_code=303)




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