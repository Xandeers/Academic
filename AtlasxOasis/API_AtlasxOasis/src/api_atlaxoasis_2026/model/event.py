from sqlalchemy import (
    BigInteger, 
    Integer, 
    Text, 
    DateTime, 
    JSON, 
    ForeignKey, 
    Identity
)

from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from typing import Optional
from datetime import datetime
from core.base import Base


class EventDB(Base):
    """Represents an event in the system.

    This class stores all information related to an event, including dates, capacity,
    descriptions, and relationships to organizers, categories, locations, media, and tickets.

    Attributes:
        id_event (int): Unique event identifier (auto-incremented primary key).
        id_organizer (int): Foreign key referencing the event organizer.
        start_date (datetime): Start date and time of the event.
        end_date (datetime): End date and time of the event.
        creation_date (datetime): Date and time when the event was created.
        event_status (str): Current status of the event (e.g., "draft", "published", "cancelled").
        max_capacity (Optional[int]): Maximum number of attendees. None if unlimited.
        description (Optional[str]): Detailed description of the event.
        metadata_ (Optional[dict]): Additional event metadata stored as JSON.
        category (List[CategoryDB]): Categories associated with the event (many-to-many).
        organizer_owner (OrganizerDB): Organizer who created the event (many-to-one).
        location (List[LocationDB]): Locations where the event takes place (many-to-many).
        media (List[MediaDB]): Media files (e.g., images, videos) linked to the event (one-to-many).
        organizer_event (List[OrganizerEventDB]): Organizers and their roles for this event (one-to-many).
        ticket_type_event (List[TicketTypeEventDB]): Ticket types available for the event (one-to-many).
        waiting_list (List[WaitingListDB]): Users on the waiting list for the event (one-to-many).
    """

    __tablename__ =  "event"

    #region Column

    id_event : Mapped[int] = mapped_column(
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
        primary_key=True,
        nullable=False
    )

    id_organizer : Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("organizer.id_organizer", ondelete="CASCADE"), 
        nullable=False
    )

    name : Mapped[str] = mapped_column(
        Text
    )

    start_date: Mapped[datetime.datetime] = mapped_column(
        DateTime
    )

    end_date: Mapped[datetime.datetime] = mapped_column(
        DateTime
    )

    creation_date: Mapped[datetime.datetime] = mapped_column(
        DateTime
    )

    event_status: Mapped[str] = mapped_column(
        Text
    )

    max_capacity: Mapped[Optional[int]] = mapped_column(
        Integer
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text
    )

    _metadata: Mapped[Optional[str]] = mapped_column(
        'metadata', 
        JSON
    )

    #endregion

    #region Relationship

    category : Mapped[list["CategoryDB"]] = relationship(
        "CategoryDB",
        secondary = "event_category",
        back_populates = "event"
    )

    organizer_owner: Mapped['OrganizerDB'] = relationship(
        'OrganizerDB', 
        back_populates = 'event_create'
    )

    location: Mapped[list['LocationDB']] = relationship(
        'LocationDB', 
        secondary = 'event_location', 
        back_populates = 'event'
    )

    media: Mapped[list['MediaDB']] = relationship(
        'MediaDB',  
        back_populates = 'event'
    )

    # On renvoie des objet de OrganizerEventDB pour avoir acces au Role
    organizer_event: Mapped[list['OrganizerEventDB']] = relationship(
        'OrganizerEventDB', 
        back_populates = 'event' 
    )
    
    ticket_type_event: Mapped[list['TicketTypeEventDB']] = relationship(
        'TicketTypeEventDB', 
        back_populates = 'event'
    )

    waiting_list: Mapped[list['WaitingListDB']] = relationship(
        'WaitingListDB', 
        back_populates = 'event'
    )

    like: Mapped[list['LikeDB']] = relationship(
        'LikeDB',
        back_populates='event'
    )

    promotion: Mapped[list['PromotionDB']] = relationship(
        'PromotionDB',
        secondary='promotion_event',
        back_populates='event'
    )

    #endregion
