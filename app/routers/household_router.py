from operator import truediv
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId

from model import Household, HouseholdUpdate

router = APIRouter()

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
def get_household(id:str, request: Request):
    if(household := request.app.database["household"].find_one({"id": id})) is not None:
        return household

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Household with ID {id} not found")

'''DELETE HOUSEHOLD'''
@router.delete("/{id}", response_description="Delete a household")
def delete_household(id:str, request: Request, response: Response):
    household_deleted = request.app.database["household"].delete_one({"id": id})

    if household_deleted.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Household with ID {id} not found")


'''UPDATE HOUSEHOLD'''
@router.put("/{id}", response_description="Update a household")
def update_household(id:str, request: Request, data: HouseholdUpdate):

    household = {k: v for k, v in data.dict().items() if v is not None}
    
    if len(household) >= 1:
        update_result = request.app.database["household"].update_one(
            {"id": id}, {"$set": household}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Household with ID {id} not found")

    if (
        existing_household := request.app.database["household"].find_one({"id":id})
    ) is not None:
        return existing_household

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Household with ID {id} not found")

    '''
    if len(household) < 1:
        return False
    household = request.app.database["household"].find_one({"id": id})
    if household:
        household_updated = request.app.database["household"].update_one({"id": id}, {"$set": data})
        if household_updated:
            return True
        return False

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Household with ID {id} not found")'''