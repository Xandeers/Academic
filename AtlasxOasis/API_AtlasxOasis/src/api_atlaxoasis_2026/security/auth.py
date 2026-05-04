from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from security.jwt import get_payload , get_jwt_field
from core.get_db import get_db
from sqlalchemy.orm import Session

from typing import Annotated
from schema.user import UserSchema
from model import UserDB

#barrier elle dit que pour obtenir le jwt il faut passer par auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token : Annotated[str, Depends(oauth2_scheme)], db : Annotated[Session, Depends(get_db)]) -> UserSchema:

    payload = get_payload(token)
    user = payload.get("sub")

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Le token ne contient pas d'utilisateur",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_token = UserSchema.model_validate_json(user)

    user = db.query(UserDB).filter(UserDB.id_user == user_token.id_user).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Le token ne contient pas d'utilisateur",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def get_user_id(token: str = Depends(oauth2_scheme)) -> int:
    return int(get_jwt_field(token, "id"))
