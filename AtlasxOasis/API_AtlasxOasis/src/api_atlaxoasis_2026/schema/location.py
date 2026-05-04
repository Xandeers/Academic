from pydantic import BaseModel
from decimal import Decimal
from pydantic.config import ConfigDict
from typing_extensions import Optional

class LocationSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_location : int
    max_capacity : int
    name : str
    address : str
    city : str
    postal_code : str
    longitude : Decimal
    latitude : Decimal
    accessibility : bool
    nearby_transport : str
    
class ResponseLocation(BaseModel):
    id_location : int
    max_capacity : Optional[int]
    name : Optional[str]
    address : Optional[str]
    city : Optional[str]
    postal_code : Optional[str]
    longitude : Optional[Decimal]
    latitude : Optional[Decimal]
    accessibility : bool
    nearby_transport : Optional[str]
    
class CreateLocation(BaseModel):
    max_capacity : Optional[int]
    name : Optional[str]
    address : Optional[str]
    city : Optional[str]
    postal_code : Optional[str]
    longitude : Optional[Decimal]
    latitude : Optional[Decimal]
    accessibility : bool
    nearby_transport : Optional[str]
