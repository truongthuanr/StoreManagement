from typing import Dict, Any
from dataclasses import asdict
from model.data.buyer import Buyer

from datetime import date, datetime
from bson.json_util import dumps
import json
from bson.dbref import DBRef

class BuyerRepository:
    def __init__(self,buyers):
        self.buyers = buyers

    def insert_buyer(self, users, details:Dict[str,Any]) ->bool:
        try:
            user = users.find_one({"_id":details["user_id"]})
            print(user)
            if user == None:
                return False
            else:
                self.buyers.insert_one(details)
        except Exception as e:
            print(e)
            return False
        return True
    
    def get_all_buyer(self):
        bs = self.buyers.find()
        [print(b) for b in self.buyers.find()]

        buyers = [asdict(Buyer(**json.loads(dumps(b)))) for b in self.buyers.find()]
        return buyers

    def get_buyer(self, id:int): 
        buyer = self.buyers.find_one({"buyer_id": id})
        return asdict(Buyer(**json.loads(dumps(buyer))))   