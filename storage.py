import pymongo

class Collection:
    """
    Initialise parameters:
    - dbhost
    - dbname
    - collection
    Methods:
    + find(name)
    + add()
    
    """
    def __init__(self, dbhost: str, dbname: str, collection: str):
        self._client = pymongo.MongoClient(dbhost)
        self._db = self._client[dbname]
        self._collection = self._db[collection]
        