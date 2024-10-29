from typing import Collection, Any, Mapping

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.synchronous.collection import Collection

def connect() -> MongoClient:
    uri = "mongodb+srv://cosmingorun69:12345678910@test1.evshv.mongodb.net/?retryWrites=true&w=majority&appName=test1"
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        # print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        # print(e)
        return None


def getTabel(client: MongoClient, dataBase: str, tabel: str) -> Collection[Mapping[str, Any] | Any]:
    database = client[dataBase]
    tabel = database[tabel]
    return tabel
