from operator import truediv
from pydoc import doc
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from typing import Optional
from model import User, Address

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

'''DELETE ALL HOUSEHOLDS'''
@router.delete("/delete_all", response_description="Delete all households")
def delete_all_household(request: Request, response: Response):
    household_deleted = request.app.database["household"].delete_many({})

    if household_deleted.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Household not found")


'''DELETE HOUSEHOLD'''
@router.delete("/{id}", response_description="Delete a household")
def delete_household(id:str, request: Request, response: Response):
    household_deleted = request.app.database["household"].delete_one({"id": id})

    if household_deleted.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Household with ID {id} not found")


'''UPDATE HOUSEHOLD'''
@router.put("/{id}", response_description="Update a household", response_model=Household)
def update_household(id:str, request: Request, data: HouseholdUpdate = Body(...)):

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

'''LIST HOUSEHOLDS OF A USER'''
@router.get("/{username}", response_description="Get the list of Households of a user", response_model=List[Household])
def list_households_by_user(username : str, request : Request, response : Response):
    households = list(request.app.database["household"].find({"host.host_username": username}, limit = 100))
    return households

'''LIST HOUSEHOLDS FILTERED BY PRICE'''
@router.get("/filter/price", response_description="Filter households by price", response_model=List[Household])
def list_households_by_price( request : Request, max_price : Optional[float], min_price : Optional[float]=0):
    households = list(request.app.database["household"].find({"price_euro_per_night":{"$gte":min_price, "$lte":max_price}}, limit=100))
    return households

'''GET USER FROM HOUSEHOLD'''
@router.get("/owners/{id}", response_description="Get user of a households host", response_model=User)
def get_use(id : str, request : Request):
    household = request.app.database["household"].find_one({"id":id})
    host_username = household["host"]["host_username"]
    host = request.app.database["user"].find_one({"username":host_username})
    return host

'''GET ADRESS OF A HOUSEHOLD'''
@router.get("/address/{id}", response_description="Get address of a household", response_model=Address)
def get_address_of_household(id : str, request : Request):
     
    household = request.app.database["household"].find_one({"id":id})
    id_addres = household["address"]["id"]
    address = request.app.database["address"].find_one({"id":id_addres})

    return address
