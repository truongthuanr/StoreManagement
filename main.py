from fastapi import FastAPI
from api import auth, product, admin, cart
from middlewares.user_context import UserContextMiddleware


app = FastAPI()

app.add_middleware(UserContextMiddleware)
app.include_router(product.router)
app.include_router(auth.router)
app.include_router(admin.router, tags=["Admin"])
app.include_router(cart.router)

