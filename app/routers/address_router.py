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

'''DELETE ADDRESS'''
@router.delete("/{id}", response_description="Delete an address")
def delete_address(id:str, request: Request, response: Response):
    address_deleted = request.app.database["address"].delete_one({"id": id})

    if address_deleted.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address not found")