from pydantic import (
    BaseModel,
    Field,
    computed_field,
)
from typing import (
    Literal,
    Optional
)
from model.follow import FollowDB
from pydantic.config import ConfigDict
class CustomerSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes= True
    )
    
    id_customer: int
    firstname: str
    lastname: str
    username : str
    email : str
    description : Optional[str]

class CreateCustomer(BaseModel):
    username: Optional[str]
    firstname: str
    lastname: str
    email: str
    description: Optional[str]
    auth_type : Literal['password', 'google', 'facebook']
    token: str

class ResponseCustomer(BaseModel):
    
    model_config= ConfigDict(
        arbitrary_types_allowed=True, # Allows using types that Pydantic doesn’t know how to handle natively (enables better typing)
        from_attributes=True, # Enables serialization/deserialization from ORM classes
    )
    
    id_customer: int
    firstname: str
    lastname: str
    username : str
    email : str
    description : Optional[str]
    
    followed_raw : list[FollowDB] = Field(
        default=[],
        exclude=True,
        validation_alias='follow'
    )
    
    follower_raw : list[FollowDB] = Field(
        default=[],
        exclude=True,
        validation_alias='followed_by'
    )
    
    @computed_field
    @property
    def nb_follower(self) -> int:
        return len(self.follower_raw)
    
    @computed_field
    @property
    def nb_followed(self) -> int:
        return len(self.followed_raw)

class UpdateCustomer(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username : Optional[str] = None
    # email : Optional[str]
    description : Optional[str] = None