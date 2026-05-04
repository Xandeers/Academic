from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from schema.user import UserSchema
from core.get_db import get_db
from security.auth import get_current_user
from security.permissions import required_role

SessionDependency = Annotated[Session, Depends(get_db)]
CurrentUserDependency = Annotated[UserSchema, Depends(get_current_user)]
FormDataDependency = Annotated[OAuth2PasswordRequestForm, Depends()]
OrganizerDependency = Annotated[UserSchema, Depends(required_role("organizer"))]
CustomerDependency = Annotated[UserSchema, Depends(required_role("customer"))]