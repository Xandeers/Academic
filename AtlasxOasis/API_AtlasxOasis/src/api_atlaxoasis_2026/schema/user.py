from pydantic import BaseModel
from typing import Optional, Literal
from pydantic.config import ConfigDict

class UserSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
    id_user: int
    type_user : str
    username : str
    email : str
    description : Optional[str]

class CreateUser(BaseModel):
    type_user: Literal['customer', 'organizer']
    name: str
    email: str
    description: Optional[str]

class CreateUserPassword(CreateUser):
    auth_type : Literal['password']
    password: str
    
class ResponseUser(BaseModel):
    
    id_user: int
    type_user : str
    username : str
    email : str
    description : Optional[str]