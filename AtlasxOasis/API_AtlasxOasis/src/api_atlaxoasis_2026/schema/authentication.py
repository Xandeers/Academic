from pydantic import BaseModel
from pydantic.config import ConfigDict

#pour lire ecrire dans la bd
class AuthenticationSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    type_auth : str
    id_user : int
    token : str     

#pour la route /login 
class LoginSchema(BaseModel):
    email: str
    password: str


#pour gerer le jwt 
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"