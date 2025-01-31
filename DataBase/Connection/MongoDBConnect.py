from typing import Optional, Mapping, Any
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection


class MongoDBConnect:
    _instance: Optional["MongoDBConnect"] = None
    client: Optional[MongoClient] = None

    def __new__(cls) -> "MongoDBConnect":
        if cls._instance is None:
            cls._instance = super(MongoDBConnect, cls).__new__(cls)
            cls._instance.client = cls._connect()  # Inițializăm `client` cu `_connect()`
        return cls._instance

    @staticmethod
    def _connect() -> Optional[MongoClient]:
        uri = "mongodb+srv://Username:Password@DBname.evshv.mongodb.net/?retryWrites=true&w=majority&appName=DBname" #se genereaza automat in aplicatia mongodb
        client = MongoClient(uri, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            print("You successfully connected to MongoDB!")
            return client
        except Exception as e:
            print("Connection failed:", e)
            return None

    def get_tabel(self, database_name: str, collection_name: str) -> Optional[Collection[Mapping[str, Any]]]:
        if self.client is None:
            print("Client is not connected.")
            return None

        database = self.client[database_name]
        collection = database[collection_name]
        return collection

    @classmethod
    def disconnect(cls):
        if cls._instance is not None and cls._instance.client is not None:
            cls._instance.client.close()
            cls._instance = None
            print("Disconnected")

