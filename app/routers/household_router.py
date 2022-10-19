from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from dotenv import dotenv_values
from typing import List

import uvicorn

from model import Household

router = APIRouter()

@router.get("/hello")
def hello_world(request: Request):
    return { "hello_world ": "hello_world"}


'''CREATE HOUSEHOLD'''
@router.post("/", response_description="Create a new household", status_code=status.HTTP_201_CREATED, response_model=Household)
def create_household(request: Request, household: Household = Body(...)):
    household = jsonable_encoder(household)
    new_household = request.app.database["household"].insert_one(household)
    created_household = request.app.database["household"].find_one(
        {"_id": new_household.inserted_id}
    )

    return created_household

'''LIST HOUSEHOLDS'''
@router.get("/",response_description="List all households", response_model=List[Household])
def list_households(request: Request):
    households = list(request.app.database["household"].find(limit=100))
    return households
    
'''GET HOUSEHOLD'''
@router.get("/{id}", response_description="Get a single household", response_model=Household)
def get_household(request: Request):
    if(household := request.app.database["household"].find_one({"_id": id})) is not None:
        return household

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Household with ID {id} not found")

'''DELETE HOUSEHOLD'''
@router.delete("/{id}", response_description="Delete a household")
def delete_household(request: Request, response: Response):
    household_deleted = request.app.database["household"].delete_one({"_id": id})

    if household_deleted.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Household with ID {id} not found")



    
