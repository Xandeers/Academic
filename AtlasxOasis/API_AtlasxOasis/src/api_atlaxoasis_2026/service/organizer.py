from fastapi import HTTPException
from schema.organizer import UpdateOrganizer
from sqlalchemy.orm import Session

from typing import Optional

from model.organizer import OrganizerDB
from model.authentication  import AuthenticationDB
from security.hashing import hash_password

def create_organizer_password(
        username:str,
        email:str,
        siret:str,
        description: Optional[str],
        password: str, 
        db: Session
    ) -> OrganizerDB:
    """Create a organizer with password authentication.

    Args:
        name (str): pseudo of the organizer
        email (str): email of the organizer
        siret (str): siret of the organizer
        description (Optional[str]): description of the organizer
        password (str): password hash of the organizer
        db (Session): database session

    Returns:
        OrganizerDB: the created organizer object
    """
    new_organizer = OrganizerDB(
        type_user= 'organizer',
        username= username,
        email= email,
        siret= siret,
        description= description
    )
    db.add(new_organizer)
    db.commit()
    db.refresh(new_organizer)

    hashed_pwd = hash_password(password)

    auth = AuthenticationDB(
        type_auth = 'password',
        id_user = new_organizer.id_organizer,
        token = hashed_pwd
    )
    db.add(auth)
    db.commit()
    db.refresh(auth)
    return new_organizer
    
def update_organizer_db(new_organizer: UpdateOrganizer, organizer_id: int, db: Session):
    old_organizer = db.query(OrganizerDB).filter(OrganizerDB.id_organizer == organizer_id).first()
    if not old_organizer:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in new_organizer.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(old_organizer, key, value)
    db.commit()
    db.refresh(old_organizer)
    return old_organizer
    
def delete_organizer_db(id_organizer : int, db: Session):
    organizer = db.query(OrganizerDB).filter(OrganizerDB.id_organizer == id_organizer).first()
    db.delete(organizer)
    db.commit()