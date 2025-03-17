from pydantic import BaseModel, validator
from bson import ObjectId
from datetime import date, datetime



class PurchaseHistoryReq(BaseModel):
    purchase_id: int
    shipping_address: str
    email: str
    date_purchased: date
    date_shipped: date 
    date_payment: date

    @validator("date_purchased")
    def date_purchased_datetime(cls, value):
        return datetime.strptime(value.strftime('%Y-%m-%dT%H:%M:%S'),  "%Y-%m-%dT%H:%M:%S")
    
    @validator('date_shipped')
    def date_shipped_datetime(cls, value):
        return datetime.strptime(value.strftime('%Y-%m-%dT%H:%M:%S'), "%Y-%m-%dT%H:%M:%S")
    
    @validator('date_payment')
    def date_payment_datetime(cls, value):
       return datetime.strptime(value.strftime('%Y-%m-%dT%H:%M:%S'), "%Y-%m-%dT%H:%M:%S")
    
    class Config:
        arbitrary_types_allowed = True
        json_encoder = {
            ObjectId:str
        }
    



        