from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional

from auth.auth import verify_access_token
from model.data.models import User
from db_config.mysql_config import sess_db  # session
from .auth import SECRET_KEY, ALGORITHM  # cấu hình JWT


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(self, tokenUrl: str = "login"):
        super().__init__(flows={}, scheme_name="OAuth2PasswordBearerWithCookie")
        self.tokenUrl = tokenUrl

    async def __call__(self, request: Request) -> Optional[str]:
        # Ưu tiên đọc từ Cookie
        token = request.cookies.get("access_token")
        if token:
            if token.startswith("Bearer "):
                return token.replace("Bearer ", "")
            return token

        # Fallback: nếu không có cookie thì thử đọc từ Header
        auth_header: str = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ", 1)[1]

        # Không có token → raise lỗi
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(sess_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token decode error")

def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user


