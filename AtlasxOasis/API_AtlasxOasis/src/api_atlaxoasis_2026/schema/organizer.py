from pydantic import (
    BaseModel,
    Field,
    computed_field
)
from typing import (
    Literal,
    Optional
)
from pydantic.config import ConfigDict
from model.follow import FollowDB

class OrganizerSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
    id_organizer: int
    username : str
    email : str
    siret : str
    description : Optional[str]
    

class CreateOrganizer(BaseModel):
    username: str
    email: str
    siret : str
    description: Optional[str]
    auth_type: Literal['password', 'google', 'facebook']
    token: str
    
class ResponseOrganizer(BaseModel):
    
    model_config= ConfigDict(
        arbitrary_types_allowed=True, # Allows using types that Pydantic doesn’t know how to handle natively (enables better typing)
        from_attributes=True, # Enables serialization/deserialization from ORM classes
    )
    
    id_organizer: int
    username : str
    email : str
    siret : str
    description : Optional[str]
    
    follow_raw : list[FollowDB] = Field(
        default=[],
        exclude=True,
        validation_alias='followed_by'
    )
    
    @computed_field
    @property
    def nb_follower(self) -> int:
        return len(self.follow_raw)
    
class UpdateOrganizer(BaseModel):
    username : Optional[str]
    # email : Optional[str] # TODO verif mail
    siret : Optional[str]
    description : Optional[str]
    