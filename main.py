from fastapi import FastAPI, Query, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel

class Reservation(BaseModel):
    name: str
    time: int
    table_number: int

client = MongoClient('mongodb://localhost', 27017)

db = client["restaurant"]
collection = db["tables"]

app = FastAPI()

@app.get("/")
def get_base():
    return "Welcome to exceed-restaurants-reservation"

@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name:str):
    lst = []
    for i in collection.find({"name":name},{"_id":0}):
        lst.append(i)
    return lst

@app.get("/reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    lst = []
    for i in collection.find({"table_number":table},{"_id":0}):
        lst.append(i)
    return lst


@app.post("/reservation")
def reserve(reservation: Reservation):
    find_previous_reserve = collection.find({"$and": [{"table": reservation.table_number},
                                                      {"time": {"&gt": reservation.time}},
                                                      {"time": {"&lt": reservation.time+1}}]})
    if len(list(find_previous_reserve)) == 0:
        collection.insert_one(dict(reservation))
    else:
        raise HTTPException(404, f"The table already reserved")


@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    find_previous_reserve = collection.find_one({"$and": [{"table": reservation.table_number},
                                                {"name": reservation.name}]})
    if len(find_previous_reserve) == 1:
        collection.insert_one(find_previous_reserve, {"$set": reservation})
    else:
        raise HTTPException(404, f"Can't find any of your previous reservation")



@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    query = {"name": name, "table_number": table_number}
    collection.delete_many(query)
    return{
        "deleted"
    }

