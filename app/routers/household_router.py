from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from dotenv import dotenv_values
import uvicorn

from B7servidorREST.app.model import Household

router = APIRouter()


@router.post("/", response_description="Create a new household", status_code=status.HTTP_201_CREATED, response_model=Household)
def create_household(request: Request, household: Household = Body(...)):
    household = jsonable_encoder(household)
    new_household = request.app.database["household"].insert_one(household)
    created_household = request.app.database["household"].find_one(
        {"_id": new_household.inserted_id}
    )

    return created_household


    
