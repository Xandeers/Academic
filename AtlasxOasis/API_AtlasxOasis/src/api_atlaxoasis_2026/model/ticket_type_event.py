from sqlalchemy import (
    BigInteger, 
    Integer, 
    Text,  
    ForeignKey, 
    Identity,
    Numeric
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from typing import Optional
from decimal import Decimal
from core.base import Base

class TicketTypeEventDB(Base):
    """
    SQLAlchemy model representing a type of ticket associated with an event.

    This class defines the characteristics of different ticket types available for an event,
    including price, label, description, and available quantity.

    Attributes:
        id_ticket_type (int):
            Primary key. Auto-incremented unique identifier for the ticket type.
        id_event (int):
            Foreign key referencing the associated event (event.id_event).
            Required (nullable=False).
        price (Optional[Decimal]):
            Price of the ticket type, stored with precision of 10 digits (2 decimal places).
            Nullable if the price is not yet determined.
        label (Optional[str]):
            Short label or name for the ticket type (e.g., 'VIP', 'Standard', 'Early Bird').
            Nullable if not specified.
        description (Optional[str]):
            Detailed description of the ticket type, including benefits or restrictions.
            Nullable if not provided.
        quantity (Optional[int]):
            Total available quantity of tickets for this type.
            Nullable if unlimited or not yet defined.
        event (EventDB):
            Many-to-one relationship with EventDB. Represents the event associated
            with this ticket type.
        ticket (List[TicketDB]):
            One-to-many relationship with TicketDB. Represents all tickets issued
            under this ticket type.
    """

    __tablename__ = 'ticket_type_event'

    #region Column

    id_ticket_type: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            always=True, 
            start=1, 
            increment=1, 
            minvalue=1, 
            maxvalue=9223372036854775807, 
            cycle=False, 
            cache=1
            ), 
        primary_key=True
    )

    id_event: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('event.id_event'), 
        nullable=False
    )

    price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2)
    )

    label: Mapped[Optional[str]] = mapped_column(
        Text
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text
    )

    quantity: Mapped[Optional[int]] = mapped_column(
        Integer
    )

    #region Relationship

    event: Mapped['EventDB'] = relationship(
        'EventDB', 
        back_populates='ticket_type_event'
    )

    ticket: Mapped[list['TicketDB']] = relationship(
        'TicketDB', 
        back_populates='ticket_type_event'
    )
    #endregion
