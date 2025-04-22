from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from model.data.models import Cart, CartItem, Product
from auth.dependencies import get_current_user
from db_config.mysql_config import sess_db
from utils.template import render_template



router = APIRouter()
templates = Jinja2Templates(directory="templates")  # template response


@router.post("/cart/add", response_class=RedirectResponse)
def add_to_cart(
    product_id: int = Form(...),
    quantity: int = Form(1),
    db: Session = Depends(sess_db),
    user = Depends(get_current_user)
):
    # Tìm hoặc tạo cart
    # Nếu user hiện tại đã có cart -> update cart
    # Nếu chưa -> tạo cart và update cart
    cart = db.query(Cart).filter_by(user_id=user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Tìm item trong cart
    # Nếu chưa có item -> add item to cart
    # Nếu có -> tăng số lượng.
    item = db.query(CartItem).filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.add(item)

    db.commit()
    return RedirectResponse(url="/cart", status_code=303)



@router.get("/cart", response_class=HTMLResponse)
def view_cart(
    request: Request,
    db: Session = Depends(sess_db),
    user=Depends(get_current_user)
):
    # Tìm cart tương ứng với user
    cart = db.query(Cart).filter_by(user_id=user.id).first()
    items = []

    if cart:
        items = (
            db.query(CartItem.id, Product.name, Product.price, CartItem.quantity)
            .join(Product, CartItem.product_id == Product.id)
            .filter(CartItem.cart_id == cart.id)
            .all()
        )

    cart_total = sum(item.price * item.quantity for item in items)

    return render_template(request, "cart/view.html", {
        "request": request,
        "items": items,
        "cart_total": cart_total,
        "user": user  # truyền user vào base để hiện lên nav bar
    })