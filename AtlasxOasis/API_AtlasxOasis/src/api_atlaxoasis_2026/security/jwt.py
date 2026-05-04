import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def create_jwt(data: dict, expires_delta: timedelta = None):

    encode = data.copy()

    maintenant = datetime.now(timezone.utc)
    if expires_delta :
        expires_date= maintenant + expires_delta
    else:
        expires_date= maintenant + timedelta(hours=24)
 
    encode.update({
        "exp":expires_date,
        "iat":maintenant
        })
    
    encoded_jwt= jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_payload(token):

    try:
        return jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.ExpiredSignatureError :
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Le token a expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )



def get_jwt_field(token, field: str):
    
    try:
        payload= get_payload(token)
        choosen_one = payload.get(field)
        
        if choosen_one is None :
            raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail= "Champs demander innexistant",
            headers={"WWW-Authenticate": "Bearer"}
            )
        
        return choosen_one 
        

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
   
