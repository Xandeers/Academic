from sqlalchemy import (
    BigInteger, 
    ForeignKey 
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column
)

from core.base import Base

class EventLocationDB(Base):
    """
    Association table linking events to their locations.

    This table implements a many-to-many relationship between EventDB and LocationDB.
    Each row represents a single event occurring at a single location.

    Attributes:
        id_location (int): Foreign key referencing the location (primary key).
        id_event (int): Foreign key referencing the event (primary key).
    """
    
    __tablename__ = "event_location"

    #region Column

    id_location : Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("location.id_location"),
        primary_key=True
    )
    
    id_event : Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("event.id_event"),
        primary_key=True
    )
    
    #endregion
