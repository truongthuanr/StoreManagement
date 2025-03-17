from fastapi import APIRouter, Depends
from db_config.pymongo_config import create_db_collections



router = APIRouter()

@router.get("/testconnect")
def test_connect(db = Depends(create_db_collections)):
    return "Connect DB"