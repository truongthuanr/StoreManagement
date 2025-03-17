from fastapi import FastAPI
from api import testconnect,buyer

app = FastAPI()


app.include_router(testconnect.router)
app.include_router(buyer.router)