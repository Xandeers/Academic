from typing import (
    Optional, 
    Any
)
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal

from model import TicketTypeEventDB



def create_ticket_type_event_db(
    
    id_event: int,
    price: Optional[Decimal],
    label: Optional[str],
    description: Optional[str],
    quantity: Optional[int],
    db: Session
) -> TicketTypeEventDB:
    """
    Crée un nouveau type de billet pour un événement dans la base de données.
    """


    new_ticket_type_event = TicketTypeEventDB(
        id_event=id_event,
        price=price,
        label=label,
        description=description,
        quantity=quantity,    
    )

    db.add(new_ticket_type_event)
    db.commit()
    db.refresh(new_ticket_type_event)

    return new_ticket_type_event


def update_ticket_type_event_db(
        db:Session,
        ticket_type_id: int,
    event_id: int,
    update_data: dict
) -> Optional[TicketTypeEventDB]:
    """
    Met à jour partiellement un type de billet en base de données.
    Retourne l'objet modifié, ou None s'il n'est pas trouvé.
    """
    ticket_type = db.query(TicketTypeEventDB).filter(
        TicketTypeEventDB.id_ticket_type == ticket_type_id,
        TicketTypeEventDB.id_event == event_id
    ).first()

    if not ticket_type:
        raise HTTPException(status_code=404, detail="Ticket type not found")
    
    for key, value in update_data.items():
        setattr(ticket_type, key, value)
    
    db.commit()
    db.refresh(ticket_type)

    return ticket_type
    
def delete_ticket_type_db(id_ticket_type: int, db: Session):
    ticket_type = db.query(TicketTypeEventDB).filter(TicketTypeEventDB.id_ticket_type == id_ticket_type).filter()
    db.delete(ticket_type)