from fastapi import FastAPI
from api import auth, product, admin

app = FastAPI()


app.include_router(product.router)
app.include_router(auth.router)
app.include_router(admin.router, tags=["Admin"])
