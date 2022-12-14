from datetime import date, datetime
from lib2to3.pgen2.token import OP
import uuid
from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from typing import Union, List, Optional
from datetime import date

class GeoJson(BaseModel):
    latitude: float
    longitude: float
    @validator("latitude") 
    def latitude_must_be_between_minus_90_and_90(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('latitude must be between -90 and 90')
        return v
    @validator("longitude")
    def longitude_must_be_between_minus_180_and_180(cls, v):
        if not -180 <= v <= 180:
            raise ValueError('longitude must be between -180 and 180')
        return v

class AddressUpdate(BaseModel):
    street: Optional[str]
    number: Optional[str]
    floor: Optional[str]
    geojson: Optional[GeoJson]
    postal_code: Optional[int]
    details: Optional[str]

    

class Address(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
    street: str
    number: str
    floor: Optional[str]
    geojson: GeoJson
    postal_code: Optional[int]
    details: Optional[str]
    @validator("geojson")
    def geojson_must_be_valid(cls, v):
        if not isinstance(v, GeoJson):
            raise ValueError('geojson must be a GeoJson')
        return v

class AddressHouseHold(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
    street: str
    number: str
    geojson: GeoJson


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
    username: str
    first_name: str
    last_name: str
    email: str
    @validator("email")
    def email_must_be_valid(cls, v):
        if not '@' in v:
            raise ValueError('email must be valid')
        return v

class HouseholdUser(BaseModel):
    host_username : str
    host_email: str
    @validator("host_email")
    def email_must_be_valid(cls, v):
        if not '@' in v:
            raise ValueError('email must be valid')
        return v

class HouseholdUserUpdate(BaseModel):
    host_username : Optional[str]
    host_email: Optional[str]
    @validator("host_email")
    def email_must_be_valid(cls, v):
        if not '@' in v:
            raise ValueError('email must be valid')
        return v

class RenterUser(BaseModel):
    renter_username : str
    renter_email: str
    @validator("renter_email")
    def email_must_be_valid(cls, v):
        if not '@' in v:
            raise ValueError('email must be valid')
        return v

class RenterUserUpdate(BaseModel):
    renter_username : Optional[str]
    renter_email: Optional[str]
    @validator("renter_email")
    def email_must_be_valid(cls, v):
        if not '@' in v:
            raise ValueError('email must be valid')
        return v

class Date(BaseModel):
    date: datetime = Field(alias="$date", default=datetime.now())
    

class Household(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
    '''HOST'''
    host: HouseholdUser
    title: str
    description: str
    '''ADDRESS'''
    address: AddressHouseHold
    photo: List[str]
    num_bathroom: int
    num_bed: int
    max_capacity: int
    price_euro_per_night: float
    rating: float
    availability: List[List[Date]]
    @validator("num_bathroom")
    def check_num_bathroom(cls, v):
        if v < 0:
            raise ValueError("num_bathroom must be positive")
        return v
    @validator("num_bed")
    def check_num_bed(cls, v):
        if v < 0:
            raise ValueError("num_bed must be positive")
        return v
    @validator("max_capacity")
    def check_max_capacity(cls, v):
        if v < 0:
            raise ValueError("max_capacity must be positive")
        return v
    @validator("price_euro_per_night")
    def check_price_euro_per_night(cls, v):
        if v < 0:
            raise ValueError("price_euro_per_night must be positive")
        return v
    @validator("rating")
    def check_rating(cls, v):
        if v < 0:
            raise ValueError("rating must be positive")
        return v
    
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
    @root_validator
    def check_start_ending_dates(cls, values):
        if values.get('ending') < values.get('start'):
            raise ValueError("ending date must be after start date")
        return values

class BookedHouseholdAddressUpdate(BaseModel):
    street: Optional[str]
    number: Optional[int]
    postal_code: Optional[int]

class BookedHouseholdUpdate(BaseModel):
    id: Optional[str]
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