from datetime import date, datetime
from lib2to3.pgen2.token import OP
import uuid
from pydantic import BaseModel, Field
from typing import Union, List, Optional

class GeoJson(BaseModel):
    latitude: float
    longitude: float

class Address(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    street: str
    number: str
    floor: Optional[str]
    geojson: GeoJson
    postal_code: str
    details: Optional[str]


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str
    first_name: str
    last_name: str
    email: str

class HouseholdUser(BaseModel):
    host_username : str
    host_email: str

class HouseholdUserUpdate(BaseModel):
    host_username : Optional[str]
    host_email: Optional[str]


class Period(BaseModel):
    start: date
    end: date


class Household(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    '''HOST'''
    host: HouseholdUser
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

class BookedHouseholdAddress(BaseModel):
    street: str
    number: int
    postal_code: int

class BookedHousehold(BaseModel):
    title: str
    address: BookedHouseholdAddress

class Booking(BaseModel):
    start: datetime
    ending: datetime
    host: HouseholdUser
    renter: HouseholdUser
    household: BookedHousehold

class BookedHouseholdAddressUpdate(BaseModel):
    street: Optional[str]
    number: Optional[int]
    postal_code: Optional[int]

class BookedHouseholdUpdate(BaseModel):
    title: Optional[str]
    address: Optional[BookedHouseholdAddress]

class BookingUpdate(BaseModel):
    start: Optional[datetime]
    ending: Optional[datetime]
    host: Optional[HouseholdUserUpdate]
    renter: Optional[HouseholdUserUpdate]
    household: Optional[BookedHouseholdUpdate]