from datetime import date
import uuid
from pydantic import BaseModel, Field
from typing import Union, List, Optional

class Address(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    street: str
    number: str
    floor: Optional[str]
    geojson: List[float]
    postal_code: str
    details: str

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str
    first_name: str
    last_name: str
    email: str

class Period(BaseModel):
    start: date
    end: date

class Household(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    '''HOST'''
    host_username : str
    host_email: str
    title: str
    description: str
    '''ADDRESS'''
    address: Address
    photo: List[str]
    num_bathroom: int
    num_bed: int
    max_capacity: int
    price_euro_per_night: float
    rating: float
    availability: List[Period]


class Booking(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    period: Period

    '''HOST'''
    host_email: str

    '''RENTER'''
    renter_username: str
    renter_email: str

    '''HOUSEHOLD'''
    household_tittle: str
    household_address_street: str
    household_address_number: int
    household_address_postal_code: str