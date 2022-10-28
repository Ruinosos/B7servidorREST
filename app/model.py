from datetime import date, datetime
from lib2to3.pgen2.token import OP
import uuid
from pydantic import BaseModel, Field, ValidationError, validator
from typing import Union, List, Optional
from datetime import date

class GeoJson(BaseModel):
    latitude: float
    longitude: float

class AddressUpdate(BaseModel):
    street: Optional[str]
    number: Optional[str]
    floor: Optional[str]
    geojson: Optional[GeoJson]
    postal_code: Optional[str]
    details: Optional[str]

class Address(BaseModel):
    street: str
    number: str
    floor: Optional[str]
    geojson: GeoJson
    postal_code: str
    details: Optional[str]


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
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
    
class RenterUser(BaseModel):
    renter_username : str
    renter_email: str

class RenterUserUpdate(BaseModel):
    renter_username : Optional[str]
    renter_email: Optional[str]


class Date(BaseModel):
    date: datetime = Field(alias="$date", default=datetime.now())
    

class Household(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
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
    availability: List[List[Date]]
    
    @validator("availability")
    def check_dates_length(cls, v):
        for i in v:
            if not len(i) == 2:
                raise ValueError("Wrong date format.")

        return v
    

class BookedHouseholdAddress(BaseModel):
    street: str
    number: int
    postal_code: int

class BookedHousehold(BaseModel):
    id : str
    title: str
    address: BookedHouseholdAddress

class Booking(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
    start: datetime
    ending: datetime
    host: HouseholdUser
    renter: RenterUser
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
    renter: Optional[RenterUserUpdate]
    household: Optional[BookedHouseholdUpdate]

class HouseholdUpdate(BaseModel):
    '''HOST'''
    host: Optional[HouseholdUserUpdate]
    title: Optional[str]
    description: Optional[str]
    '''ADDRESS'''
    address: Optional[AddressUpdate]
    photo: Optional[List[str]]
    num_bathroom: Optional[int]
    num_bed: Optional[int]
    max_capacity: Optional[int]
    price_euro_per_night: Optional[float]
    rating: Optional[float]
    availability: Optional[List[List[Date]]]