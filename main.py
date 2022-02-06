from fastapi import FastAPI, HTTPException
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


@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name:str):
    pass


@app.get("reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    pass


@app.post("/reservation")
def reserve(reservation: Reservation):
    find_previous_reserve = collection.find({"$and": [{"table": reservation.table_number},
                                                      {"time": {"&gt": reservation.time}},
                                                      {"time": {"&lt": reservation.time+1}}]})
    if len(find_previous_reserve) == 0:
        collection.insert_one(reservation)
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
def cancel_reservation(name: str, table_number: int):
    pass
