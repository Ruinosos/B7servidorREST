from pydantic import BaseModel
from typing import Union, List, Optional

class Address(BaseModel):
    street: str
    number: str
    floor: Optional[str]
    coordinates: List[float, float]
    details: str

class Household(BaseModel):
    name: str
    description: Optional[str] = None
    num_rooms: int
    num_bathrooms: int
    num_beds: int
    photo: Optional[str] = None
    address: Address
