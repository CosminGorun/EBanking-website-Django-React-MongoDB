from typing import Collection, Any, Mapping, List


from pymongo.synchronous.collection import Collection

from DataBase.DB_Data.Person import Person


def addPerson(tabel:Collection[Mapping[str, Any] | Any],person:Person):
    tabel.insert_one(person.toDic())

def getAllPerson(tabel:Collection[Mapping[str, Any] | Any])-> list[Person]:
    colPers=[]
    for person in tabel.find():
        newPers=Person(person['name'],person['ages'],person['gender'])
        colPers.append(newPers)
    return colPers