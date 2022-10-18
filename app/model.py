from datetime import date
from pydantic import BaseModel
from typing import Union, List, Optional

class Address(BaseModel):
    street: str
    number: str
    floor: Optional[str]
    geojson: List[float]
    postal_code: str
    details: str

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str

class Period(BaseModel):
    start: date
    end: date

class Household(BaseModel):
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