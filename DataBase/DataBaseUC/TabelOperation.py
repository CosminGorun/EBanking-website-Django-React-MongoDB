from typing import Mapping, Any
from pymongo.synchronous.collection import Collection
from DataBase.DB_Data.Person import Person


class DataBaseTabel:
    def __init__(self,tabel:Collection[Mapping[str, Any] | Any]):
        self.__tabel = tabel

    def add(self, obj):
        self.__tabel.insert_one(obj.toDic())

    def getAll(self,cls):
        # cls=obj.__class__
        element=[]
        for contor in self.__tabel.find():
            newEl=cls.__new__(cls)
            for field_name in cls.__fields__:
                if field_name in contor:
                    setattr(newEl,field_name,contor[field_name])
            element.append(newEl)  
        return element

    def deleteOne(self,tupla:{str:str}):
        self.__tabel.delete_one(tupla)

    def deleteAll(self,tupla:{str:str}):
        self.__tabel.delete_many(tupla)

    def updateOne(self,element,update):
        self.__tabel.update_one(element,{'$set':update})

    def updateAll(self,element,update):
        self.__tabel.update_many(element,{'$set':update})

    def findOneBy(self,tupla:{str:str})->object:
        return self.__tabel.find_one(tupla)

    def findAllBy(self,tupla:{str:str})->object:
        return self.__tabel.find(tupla)



