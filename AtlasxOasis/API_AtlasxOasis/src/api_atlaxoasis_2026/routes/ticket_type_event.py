from fastapi import (
    APIRouter, 
    Depends,
    HTTPException, 
    status,
)
from typing import (
    Annotated
)
from sqlalchemy.orm import Session
from core.get_db import get_db
from schema.ticket_type_event import TicketTypeEventSchema, TicketTypeEventUpdateSchema
from model.event import EventDB
from model.ticket_type_event import TicketTypeEventDB
from security.permissions import verify_event_owner
from service.ticket_type_event import create_ticket_type_event_db , update_ticket_type_event_db

SessionDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/ticket_type_event",
    tags=["Ticket type"]
)


@router.get("/{event_id}", response_model=list[TicketTypeEventSchema])
async def get_ticket_types_for_event(
    event_id: int,
    db: SessionDependency
):
    """
    Récupère tous les types de billets disponibles pour un événement spécifique.
    """
    ticket_types = db.query(TicketTypeEventDB).filter(
        TicketTypeEventDB.id_event == event_id
    ).all()

    return ticket_types



@router.post("/{event_id}",)
async def post_ticket_types_for_event(
    event_id : int,
    data : TicketTypeEventSchema,
    db: SessionDependency,
    event: EventDB = Depends(verify_event_owner),

):
    new_ticket_type = create_ticket_type_event_db(event_id=event.id_event,
                                                  price=data.price,
                                                  label=data.label,
                                                  description=data.description,
                                                  quantity=data.quantity,
                                                  db=db)
    return new_ticket_type



@router.patch("/{event_id}/{ticket_type_id}", response_model=TicketTypeEventSchema)
async def patch_ticket_type_for_event(
    event_id: int,
    ticket_type_id: int,
    data: TicketTypeEventUpdateSchema, 
    db: SessionDependency,
    event: EventDB = Depends(verify_event_owner), 
):
    update_data_dict = data.model_dump(exclude_unset=True)

    updated_ticket = update_ticket_type_event_db(
        db=db,
        ticket_type_id=ticket_type_id,
        event_id=event.id_event,
        update_data=update_data_dict
    )

    if not updated_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket Type NOT FOUND"
        )

    return updated_ticket


@router.delete("/{event_id}/{ticket_type_id}")
async def delete_ticket_type_for_event(
    event_id: int,
    ticket_type_id: int,
    db: SessionDependency,
    event: EventDB = Depends(verify_event_owner),
):
    
    delete_ticket_type_event= db.query(TicketTypeEventDB).filter(
        TicketTypeEventDB.id_event == event_id,
        TicketTypeEventDB.id_ticket_type == ticket_type_id
     ).first()

    if not delete_ticket_type_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket Type NOT FOUND")
    

    db.delete(delete_ticket_type_event)
    db.commit()

    return {"message": f" Type de Ticket on bien été supprimé"}
