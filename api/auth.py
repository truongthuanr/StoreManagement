from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
# from bcrypt import hashpw, checkpw,gensalt
from db_config.mysql_config import SessionFactory
from model.data.models import User  # Giả sử bạn có models.User đã định nghĩa
from model.request.login import LoginReq
from fastapi.security import OAuth2PasswordRequestForm
from db_config.mysql_config import sess_db
from auth.auth import create_access_token, verify_access_token


router = APIRouter()
templates = Jinja2Templates(directory="templates")  # template response

# def sess_db():
#     db = SessionFactory()
#     try:
#         yield db
#     finally:
#         db.close()

@router.get("/register", response_class=HTMLResponse)
def get_register_page(request: Request):
    return templates.TemplateResponse("user/register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
def post_register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(sess_db)
):

    existing_user = db.query(User).filter_by(email=email).first()
    if existing_user:
        return HTMLResponse(
            content="<div class='text-red-600'>Email đã được đăng ký.</div>",
            status_code=400
        )

    hashed_password = bcrypt.hash(password)
    new_user = User(name=name, email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # return HTMLResponse(
    #     content="<div class='text-green-600'>Tạo tài khoản thành công!</div>",
    #     status_code=200
    # ) 

    return RedirectResponse(url="/login", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("user/login.html", {"request": request})

@router.post("/login")
def login(
    request: Request,
    db: Session = Depends(sess_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not bcrypt.verify(form_data.password, user.password_hash):
        return templates.TemplateResponse("user/login.html", {
            "request": request,
            "message": "Email hoặc mật khẩu không đúng",
            "message_type": "error"
        })

    access_token = create_access_token(data={"sub": str(user.id)})
    response = RedirectResponse(url="/products", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response