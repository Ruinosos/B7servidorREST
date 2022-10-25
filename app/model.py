from datetime import date
from lib2to3.pgen2.token import OP
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
    host_username: str
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


class Renter(BaseModel):
    username: str
    email: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "username": "",
            "email": "pedro@gmail.com"
        }


class Renter(BaseModel):
    username: str
    email: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "username": "",
            "email": "pedro@gmail.com"
        }

class BookedHouseholdAddress(BaseModel):
    street: str
    number: str
    postal_code: str
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "street": "C/Garcilaso de la Vega",
                "number": "30",
                "postal_code": "29007"
        }


class BookedHousehold(BaseModel):
    id: Optional[str]
    title: str
    address: BookedHouseholdAddress

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "title": "Piso en Teatinos",
            "address": {
                "street": "C/Garcilaso de la Vega",
                "number": "30",
                "postal_code": "29007"
            }
        }

class Booking(BaseModel):
    id: Optional[str]
    start: str = Field(...)
    ending: str = Field(...)
    host_email: str = Field(...)
    renter: Renter = Field(...)
    household: BookedHousehold = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "id": "1",
            "start": "22/10/2022",
            "ending": "23/10/2022",
            "host_email": "jose@gmail.com",
            "renter": {
                "username": "carlos1234",
                "email": "carlos@gmail.com"
            },
            "household": {
                "title": "Piso en Teatinos",
                "address": {
                    "street": "C/Garcilaso de la Vega",
                    "number": "30",
                    "postal_code": "29007"
                }
            }
        }
