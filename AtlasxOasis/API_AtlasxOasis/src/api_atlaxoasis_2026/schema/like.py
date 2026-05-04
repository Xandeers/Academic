from model.event import EventDB
from pydantic import BaseModel
from datetime import datetime
from pydantic.config import ConfigDict
from schema.event import ResponseEventSchema

class LikeSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_customer : int
    id_event : int
    date_like : datetime


class CreateLike(BaseModel):

    id_customer : int
    id_event : int
    
class ResponseLikeCustomer(BaseModel):
    
    date_like: datetime
    event: ResponseEventSchema