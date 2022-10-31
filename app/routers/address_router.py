from email.headerregistry import Address
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from model import Address
from typing import List
from typing import Optional

router = APIRouter()

@router.post("/", response_description="Create a new address", status_code=status.HTTP_201_CREATED, response_model=Address)
def create_address(request: Request, address: Address = Body(...)):

    address = jsonable_encoder(address)
    new_address = request.app.database["address"].insert_one(address)
    created_address = request.app.database["address"].find_one(
        {"_id": new_address.inserted_id}
    )

    return created_address