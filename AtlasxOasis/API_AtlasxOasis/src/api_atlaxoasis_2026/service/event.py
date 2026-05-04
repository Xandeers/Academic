from typing import (
    Optional, 
    Any
)
from datetime import datetime
from schema.event import UpdateEventSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException

from model import (
    MediaDB,
    LocationDB,
    CategoryDB,
    EventDB,
    TicketTypeEventDB,
    PromotionDB
)

def create_event_db(
        id_organizer: int,
        name : str,
        start_date : datetime,
        end_date : datetime,
        creation_date: datetime,
        event_status : str,
        max_capacity : Optional[int],
        description : Optional[str],
        metadata : Optional[dict[str, Any]],
        db: Session
) -> EventDB:
    new_event = EventDB(
        id_organizer = id_organizer,
        name = name,
        start_date = start_date,
        end_date = end_date,
        creation_date = creation_date,
        event_status = event_status,
        max_capacity = max_capacity,
        description = description,
        metadata = metadata
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def delete_event_db(id_event: int, db: Session):
    event = db.query(EventDB).filter(EventDB.id_event == id_event).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()

def add_category_to_event_db(id_event : int, id_category : int, db: Session) -> EventDB:
    event = db.query(EventDB).filter(EventDB.id_event == id_event).first()
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    category = db.query(CategoryDB).filter(CategoryDB.id_category == id_category).first()
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    if category not in event.category:
        event.category.append(category)
    db.commit()
    return event

def add_location_to_event_db(id_event: int, id_location: int, db: Session) -> EventDB:
    event = db.query(EventDB).filter(EventDB.id_event == id_event).first()
    if not event:
        raise HTTPException(404, "event not found")
    location = db.query(LocationDB).filter(LocationDB.id_location == id_location).first()
    if not location:
        raise HTTPException(status_code=404, detail="location not found")
    if location not in event.location:
        event.location.append(location)
    db.commit()
    return event

def add_media_to_event_db(id_event: int, id_media: int, db: Session) -> EventDB:
    event = db.query(EventDB).filter(EventDB.id_event == id_event).first()
    if not event:
        raise HTTPException(404, "event not found")
    media = db.query(MediaDB).filter(MediaDB.id_media == id_media).first()
    if not media:
        raise HTTPException(status_code=404, detail="media not found")
    if media not in event.media:
        event.media.append(media)
    db.commit()
    return event

def add_ticket_type_to_event_db(id_event: int, id_ticket_type: int, db: Session) -> EventDB:
    event = db.query(EventDB).filter(EventDB.id_event == id_event).first()
    if not event:
        raise HTTPException(404, "event not found")
    ticket_type = db.query(TicketTypeEventDB).filter(TicketTypeEventDB.id_ticket_type == id_ticket_type).first()
    if not ticket_type:
        raise HTTPException(status_code=404, detail="ticket type not found")
    if ticket_type not in event.ticket_type:
        event.ticket_type.append(ticket_type)
    db.commit()
    return event

def add_promotion_to_event_db(id_event: int, id_promotion: int, db: Session) -> EventDB:
    event = db.query(EventDB).filter(EventDB.id_event == id_event).first()
    if not event:
        raise HTTPException(404, "event not found")
    promotion = db.query(PromotionDB).filter(PromotionDB.id_promotion == id_promotion).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="promotion not found")
    if promotion not in event.promotion:
        event.promotion.append(promotion)
    db.commit()
    return event
    
def update_event_db(new_event: UpdateEventSchema, event_id: int, db: Session):
    old_event = db.query(EventDB).filter(EventDB.id_event == event_id).first()
    if not old_event:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in new_event.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(old_event, key, value)
    db.commit()
    db.refresh(old_event)
    return old_event
