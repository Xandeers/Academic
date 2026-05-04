from datetime import datetime
from model.event import EventDB
from model.like import LikeDB
from model.user import UserDB
from sqlalchemy.orm import Session


def create_like(id_customer: int, id_event: int, db: Session):
    
    date_now = datetime.now()
    
    new_like = LikeDB(
        id_customer= id_customer,
        id_event= id_event,
        date_like= date_now
    )
    
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
def delete_like(id_customer: int, id_event: int, db: Session):
    like = (db.query(LikeDB)
        .filter(LikeDB.id_customer == id_customer and 
            LikeDB.id_event == id_event)
        .first()
    )
    if like is None:
        raise ValueError("Like not found")
    db.delete(like)
    db.commit()
    