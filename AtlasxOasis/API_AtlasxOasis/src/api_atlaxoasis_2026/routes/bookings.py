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
from sqlalchemy import func
from core.dependencies import CustomerDependency
from core.get_db import get_db
from schema.bookings import BookingSchema, BookingResumeSchema

from model.event import EventDB
from model.ticket_type_event import TicketTypeEventDB
from model.payment import PaymentDB
from model.ticket import TicketDB

from security.auth import get_user_id

from datetime import datetime, timezone


SessionDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post("/{event_id}")
async def create_booking(
    event_id: int,
    booking_data: BookingSchema,
    db: SessionDependency,
    user_id: CustomerDependency
):

    """Route to create a booking.

    Args:
        even_id (int): The ID of the event to retrieve
        db (SessionDependency): The database session
        user : jwt

    Returns:
        BookingSchema: The retrieved customer object
    """

    #check type de billet
    ticket_type=db.query(TicketTypeEventDB).filter(
        TicketTypeEventDB.id_ticket_type == booking_data.id_ticket_type,
        TicketTypeEventDB.id_event == event_id
    ).first()

    if not ticket_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Type de billet introuvable pour cette event"
        )

    #check stock
    if ticket_type.quantity < booking_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock insuffisant pour cette quantité"
        )

    

    total_price= ticket_type.price * booking_data.quantity

    #on gere la table payment 
    new_payment= PaymentDB(
            
        id_user=user_id.id_user,
        price=total_price,
        status_amount="en attente",
        status_payment="en attente",
        date_payment=datetime.now(timezone.utc),
        methode_payment="carte_bancaire"

    )
    db.add(new_payment)
    db.flush()

    #on va gerer la table sale_object
    for _ in range(booking_data.quantity):
           
        new_ticket=TicketDB(

            id_payment=new_payment.id_payment, 
            id_ticket_type=ticket_type.id_ticket_type,
            status_ticket="en attente"
        )
        db.add(new_ticket)
        
    ticket_type.quantity -= booking_data.quantity


    db.commit()

    return {
        "message": "Réservation créée avec succès. En attente de paiement.",
        "payment_id": new_payment.id_payment,
        "total_price": total_price,
        "tickets_reserved": booking_data.quantity
    }
    



@router.get("/my_bookings", response_model=list[BookingResumeSchema])
async def get_My_Bookings(
    db: SessionDependency,
    user_id: CustomerDependency
):

    resultat=db.query(EventDB.id_event,
                      TicketTypeEventDB.id_ticket_type,
                      func.count(TicketDB.id_ticket).label("quantity"),
                      TicketDB.status_ticket,
                      ).join(
                          TicketTypeEventDB, EventDB.id_event == TicketTypeEventDB.id_event
                      ).join(
                          TicketDB, TicketTypeEventDB.id_ticket_type == TicketDB.id_ticket_type
                      ).join(
                          PaymentDB, TicketDB.id_payment == PaymentDB.id_payment
                      ).filter(
                          PaymentDB.id_user == user_id.id_user
                      ).group_by(
                          EventDB.id_event,
                          TicketTypeEventDB.id_ticket_type,
                          TicketDB.status_ticket
                      ).all()

    return resultat


@router.delete("/{event_id}")
async def delete_x_bookings(
    db: SessionDependency,
    event_id: int,
    id_ticket_type: int,
    quantity: int,
    user_id: CustomerDependency,
):
    ticket_to_delete=db.query(TicketDB
                 ).join(
                    PaymentDB, TicketDB.id_payment == PaymentDB.id_payment
                 ).join(
                    TicketTypeEventDB, TicketDB.id_ticket_type == TicketTypeEventDB.id_ticket_type
                 ).filter(
                     PaymentDB.id_user == user_id.id_user,
                     PaymentDB.status_payment == "en attente",
                     TicketTypeEventDB.id_event == event_id,
                     TicketDB.id_ticket_type == id_ticket_type
                 ).limit(quantity).all()


    if len(ticket_to_delete)< quantity :
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE
                            ,detail="Impossible : Vous ne possédez pas autant de billets pour cet événement."
                            )
    
    
    
    ticket_type=db.query(TicketTypeEventDB
                   ).filter(
                       TicketTypeEventDB.id_ticket_type == id_ticket_type
                   ).first()

    for ticket in ticket_to_delete :

        payment = db.query(PaymentDB).filter(PaymentDB.id_payment == ticket.id_payment).first()

        if payment and ticket_type:
            payment.price -= ticket_type.price

        db.delete(ticket)

    if ticket_type:
        ticket_type.quantity += quantity

    db.commit()

    return {"message": f"{quantity} billet(s) annulé(s) avec succès. Le stock a été mis à jour."}

