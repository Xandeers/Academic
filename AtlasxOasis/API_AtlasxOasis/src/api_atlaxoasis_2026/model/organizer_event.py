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
from core.base import Base

class OrganizerEventDB(Base):
    """
    SQLAlchemy association table for the many-to-many relationship between EventDB and OrganizerDB.

    This table acts as a junction to map organizers to events, allowing for additional
    attributes (such as 'role') to be stored on the relationship itself.

    Attributes:
        id_event (int):
            Composite primary key. Foreign key referencing the associated event (event.id_event).
        id_organizer (int):
            Composite primary key. Foreign key referencing the associated organizer (organizer.id_organizer).
        role (Optional[str]):
            Describes the organizer's role in the context of this event (e.g., 'main organizer',
            'co-organizer', 'volunteer'). Nullable if no role is specified.
        event (EventDB):
            One-to-one relationship with EventDB. Provides navigation from the association
            record to the full event details.
        organizer (OrganizerDB):
            One-to-one relationship with OrganizerDB. Provides navigation from the association
            record to the full organizer details.
    """

    __tablename__ = 'organizer_event'

    #region Column

    id_event: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("event.id_event"),
        primary_key=True
    )

    id_organizer: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("organizer.id_organizer"),
        primary_key=True
    )

    role: Mapped[Optional[str]] = mapped_column(
        Text
    )

    #endregion

    #region Relationship

    event: Mapped['EventDB'] = relationship(
        'EventDB', 
        back_populates='organizer_event'
    )

    organizer: Mapped['OrganizerDB'] = relationship(
        'OrganizerDB', 
        back_populates='organizer_event'
    )

    #endregion

