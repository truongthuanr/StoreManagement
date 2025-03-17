from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

# from model.request.buyer import BuyerReq, PurchaseHistoryReq, PurchaseStatusReq
from repository.buyer import BuyerRepository
from db_config.pymongo_config import create_db_collections

from datetime import date, datetime
from json import dumps, loads
from bson import ObjectId

router = APIRouter()

def json_serialize_date(obj):
    if isinstance(obj,(date,datetime)):
        return str(obj)
    raise TypeError (f"The type {type(obj)} not serializable.")

def json_serialize_oid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj,date):
        return obj.isoformat()
    raise TypeError(f"The type {type(obj)} not serializable.")


@router.get("/buyer/list/all")
def list_all_buyer(db=Depends(create_db_collections)):
    repo:BuyerRepository = BuyerRepository(db["buyers"])
    buyers = repo.get_all_buyer()
    return loads(dumps(buyers, default=json_serialize_oid))

