from pymongo import MongoClient

def create_db_collections():
    client = MongoClient('mongodb://localhost:27017')
    try:
        db = client.store
        buyers = db.buyer
        print(f"{type(buyers)=}")

        print("===== Connect =====")
        yield {"buyers":buyers}
    finally:
        client.close()