from schema.user import UserSchema
from core.get_db import get_db
from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from model.event import EventDB
from security.auth import get_user_id

from schema.user import UserSchema

def required_role(*role : str):
    from core.dependencies import CurrentUserDependency # Avoid circular imports by importing locally
    def checker(current_user: CurrentUserDependency) -> UserSchema:
        if current_user.type_user not in role:
            role_str = " or ".join(role)
            raise HTTPException(status_code=403, detail=f"You need to be an {role_str}")
        return current_user
    return checker

 


async def verify_event_owner(
    event_id: int, 
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id) 
) -> EventDB:
    """
    Vérifie que l'événement existe ET que l'utilisateur connecté en est le propriétaire.
    Retourne l'objet EventDB si tout est bon pour éviter de refaire la requête SQL.
    """

    event = db.query(EventDB).filter(EventDB.id_event == event_id).first()

    #verif 1
    if not event :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event Not Found."
        )
    
    #verif 2
    if not event.id_organizer == user_id :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Your are NOT the Owner"
        )

    return event