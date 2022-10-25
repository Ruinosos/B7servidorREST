from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId
from model import Booking,BookingUpdate
import datetime

router = APIRouter()

'''LIST BOOKINGS'''
@router.get("/",response_description="List all bookings", response_model=List[Booking])
def list_bookings(request: Request):
    bookings = list(request.app.database["booking"].find(limit=100))
    return bookings

'''GET BOOKING'''
@router.get("/{id}", response_description="Get a single booking", response_model=Booking)
def get_booking(id:str, request: Request):
    if(booking := request.app.database["booking"].find_one({"_id":ObjectId(id)})):
        return booking

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with ID {id} not found")

'''CREATE BOOKING'''
@router.post("/", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=Booking)
def create_household(request: Request, Booking: Booking = Body(...)):

    Booking = jsonable_encoder(Booking)
    new_booking= request.app.database["booking"].insert_one(Booking)
    created_booking = request.app.database["booking"].find_one(
        {"_id": new_booking.inserted_id}
    )

    return created_booking


'''UPDATE BOOKING '''
@router.put("/{id}", response_description="Update a book", response_model=Booking)
def update_book(id: str, request: Request, booking: BookingUpdate = Body(...)):
    booking = {k: v for k, v in booking.dict().items() if v is not None}

    if len(booking) >= 1:
        update_result = request.app.database["booking"].update_one(
            {"_id": ObjectId(id)}, {"$set": booking}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

    if (
        existing_book := request.app.database["booking"].find_one({"_id":ObjectId(id)})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")


'''DELETE BOOKING'''
@router.delete("/{id}", response_description="Delete a booking")
def delete_booking(id:str,request: Request, response: Response):
    booking_deleted = request.app.database["booking"].delete_one({"_id": ObjectId(id)})

    if booking_deleted.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with ID {id} not found")

'''LIST ACTIVE BOOKINGS'''
@router.get("_actives",response_description="List all active bookings", response_model=List[Booking])
def list_bookings(request: Request):
    active_bookings = list(request.app.database["booking"].find({
    "ending": {
        "$gte": str(datetime.datetime.now())
    }},limit=100))
    return active_bookings