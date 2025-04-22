from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from jose import jwt, JWTError
from model.data.models import User
from db_config.mysql_config import sess_db

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class UserContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None
        token = request.cookies.get("access_token")

        if token and token.startswith("Bearer "):
            try:
                token_value = token.split(" ")[1]
                payload = jwt.decode(token_value, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = int(payload.get("sub"))
                db = next(sess_db())
                user = db.query(User).filter(User.id == user_id).first()
                request.state.user = user
            except (JWTError, ValueError):
                pass

        response = await call_next(request)
        return response
