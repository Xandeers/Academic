from sqlalchemy import (
    BigInteger, 
    Text, 
    ForeignKey 
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from typing import Optional
from model.sale_object import SaleObjectDB
from model.ticket_type_event import TicketTypeEventDB

class TicketDB(SaleObjectDB):
    """
    SQLAlchemy model representing an individual ticket, inheriting from SaleObjectDB.

    Extends the base sale object model with ticket-specific attributes and relationships.
    This class represents individual tickets issued for events, linked to a specific ticket type.

    Attributes:
        id_ticket (int):
            Primary key. Foreign key referencing the base sale object (sale_object.id_sale_object).
            Inherits all sale object attributes from SaleObjectDB.
        id_ticket_type (int):
            Foreign key referencing the ticket type (ticket_type_event.id_ticket_type).
            Required (nullable=False).
        status_status (Optional[str]):
            Current status of the ticket (e.g., 'valid', 'used', 'cancelled', 'refunded').
            Nullable if not yet defined.
        ticket_type_event (TicketTypeEventDB):
            Many-to-one relationship with TicketTypeEventDB. Represents the ticket type
            associated with this individual ticket.
    """

    __tablename__ = 'ticket'

    #region Column

    id_ticket: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('sale_object.id_sale_object'), 
        primary_key=True
    )

    id_ticket_type: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('ticket_type_event.id_ticket_type'),
        nullable=False
    )

    status_ticket: Mapped[Optional[str]] = mapped_column(
        Text
    )

    #endregion

    __mapper_args__ = {
        "polymorphic_identity": "ticket",
    }

    #region Relationship

    ticket_type_event: Mapped['TicketTypeEventDB'] = relationship(
        'TicketTypeEventDB', 
        back_populates='ticket'
    )

    #endregion
    