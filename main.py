from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api import auth, product, admin, cart
from middlewares.user_context import UserContextMiddleware



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(UserContextMiddleware)
app.include_router(product.router)
app.include_router(auth.router)
app.include_router(admin.router, tags=["Admin"])
app.include_router(cart.router)
