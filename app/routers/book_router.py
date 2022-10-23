from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from dotenv import dotenv_values
from typing import List

import uvicorn

from model import Booking

router = APIRouter()

'''LIST BOOKINGS'''
@router.get("/",response_description="List all bookings", response_model=List[Booking])
def list_bookings(request: Request):
    bookings = list(request.app.database["booking"].find(limit=100))
    return bookings

'''GET BOOKING'''
@router.get("/{id}", response_description="Get a single booking", response_model=Booking)
def get_booking(request: Request):
    if(booking := request.app.database["booking"].find_one({"_id": id})) is not None:
        return booking

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with ID {id} not found")

'''DELETE BOOKING'''
@router.delete("/{id}", response_description="Delete a booking")
def delete_booking(request: Request, response: Response):
    booking_deleted = request.app.database["booking"].delete_one({"_id": id})

    if booking_deleted.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with ID {id} not found")