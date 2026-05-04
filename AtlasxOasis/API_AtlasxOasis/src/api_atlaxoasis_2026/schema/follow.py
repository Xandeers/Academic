from model.customer import CustomerDB
from pydantic import BaseModel, Field, computed_field
from datetime import datetime
from typing import Optional
from pydantic.config import ConfigDict
from schema.customer import ResponseCustomer
from schema.user import ResponseUser

class FollowSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_follower_customer : int
    id_followed_user : int
    date_follow : Optional[datetime] = None
    status_follow : Optional[str] = None

class CreateFollow(BaseModel):
    
    status_follow : Optional[str] = None

class ResponseFollow(BaseModel):
    
    id_follower_customer : int
    id_followed_user : int
    date_follow : Optional[datetime] = None
    status_follow : Optional[str] = None

class ResponseFollower(BaseModel):
    
    date_follow : Optional[datetime] = None
    status_follow : Optional[str] = None
    follower_customer: Optional[ResponseCustomer]

class ResponseFollowed(BaseModel):
    
    date_follow : Optional[datetime] = None
    status_follow : Optional[str] = None
    followed_user: Optional[ResponseUser]
        