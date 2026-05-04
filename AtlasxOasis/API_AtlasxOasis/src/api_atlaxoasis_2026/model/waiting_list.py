from sqlalchemy import (
    BigInteger,  
    Text, 
    DateTime, 
    ForeignKey, 
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from typing import Optional
from datetime import datetime
from core.base import Base

class WaitingListDB(Base):
    """
    SQLAlchemy association model representing a customer's position on an event waiting list.

    This class acts as a junction table linking customers to events they are waitlisted for,
    with additional metadata about their waitlist status and priority.

    Attributes:
        id_customer (int):
            Composite primary key. Foreign key referencing the customer (customer.id_customer).
        id_event (int):
            Composite primary key. Foreign key referencing the event (event.id_event).
        added_date (Optional[datetime]):
            Date and time when the customer was added to the waiting list.
            Nullable if not recorded.
        status_waiting (Optional[str]):
            Current status of the waitlist entry (e.g., 'pending', 'notified', 'expired').
            Nullable if not yet defined.
        type_priority (Optional[str]):
            Priority type for the waitlist entry (e.g., 'standard', 'priority', 'vip').
            Nullable if no priority is assigned.
        customer (CustomerDB):
            Many-to-one relationship with CustomerDB. Represents the customer
            on the waiting list.
        event (EventDB):
            Many-to-one relationship with EventDB. Represents the event
            for which the customer is waitlisted.
    """

    __tablename__ = 'waiting_list'

    #region Column

    id_customer: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('customer.id_customer'),
        primary_key=True
    )

    id_event: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('event.id_event'),
        primary_key=True
    )

    added_date: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime
    )

    status_waiting: Mapped[Optional[str]] = mapped_column(
        Text
    )

    type_priority: Mapped[Optional[str]] = mapped_column(
        Text
    )

    #endregion

    #region Relationship

    customer: Mapped['CustomerDB'] = relationship(
        'CustomerDB', 
        back_populates='waiting_list'
    )

    event: Mapped['EventDB'] = relationship(
        'EventDB', 
        back_populates='waiting_list'
    )

    #endregion
    