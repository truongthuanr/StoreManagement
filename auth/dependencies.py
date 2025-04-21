from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from auth.auth import verify_access_token
from models import User
from db_config.mysql_config import sess_db  # session
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(sess_db)) -> User:
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")
    
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    return user
