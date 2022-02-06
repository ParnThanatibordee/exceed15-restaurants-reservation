from fastapi import FastAPI
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
    pass


@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    pass


@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number: int):
    pass
