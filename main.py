from fastapi import FastAPI
from api import auth, testconnect,product

app = FastAPI()


app.include_router(testconnect.router)
# app.include_router(buyer.router)
app.include_router(product.router)
app.include_router(auth.router)
