from fastapi import (
    APIRouter,
    HTTPException
)
from core.dependencies import (
    SessionDependency,
    CurrentUserDependency,
    FormDataDependency
)
from security.jwt import create_jwt
from security.hashing import check_password
from schema.user import UserSchema
from model.authentication import AuthenticationDB
from model.user import UserDB
import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get('/me', response_model=UserSchema)
async def get_me(current_user: CurrentUserDependency) -> UserSchema:
    return current_user

@router.post('/login')
async def login(form_data: FormDataDependency, db: SessionDependency):

    error_message = "Incorrect email or password"

    user = db.query(UserDB).filter(UserDB.email == form_data.username).first()
    if not user:
        logger.warning(f"Failed login attempt for email: {form_data.username}")
        raise HTTPException(status_code=400, detail=error_message)

    auth = db.query(AuthenticationDB).filter(AuthenticationDB.id_user == user.id_user and AuthenticationDB.type_auth == 'password').first()
    if not auth:
        logger.warning(f"No password authentication found for email: {form_data.username}")
        raise HTTPException(status_code=400, detail=error_message)

    if not check_password(form_data.password, auth.token):
        logger.warning(f"Failed login attempt for email: {form_data.username}")
        raise HTTPException(status_code=400, detail=error_message)

    token = create_jwt({"sub": UserSchema.model_validate(user).model_dump_json()})

    return {"access_token": token, "token_type": "bearer"}
