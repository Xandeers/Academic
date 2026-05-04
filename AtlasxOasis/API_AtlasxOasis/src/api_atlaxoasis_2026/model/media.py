from sqlalchemy import (
    BigInteger, 
    Text, 
    DateTime,  
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

class MediaDB(Base):
    """
    SQLAlchemy model representing a media entity in the database.

    This class stores metadata and relationships for media files (images, videos, documents)
    associated with users, events, or locations.

    Attributes:
        id_media (int):
            Primary key. Auto-incremented unique identifier for the media.
        label (str):
            Human-readable label or title for the media. Required.
        description (Optional[str]):
            Detailed description of the media content. Nullable if not provided.
        format_media (Optional[str]):
            File format or MIME type of the media (e.g., 'image/jpeg', 'video/mp4').
            Nullable if unknown.
        url (Optional[str]):
            URL or path to access the media file. Nullable if the file is stored locally
            or the URL is not yet generated.
        usage_media (Optional[str]):
            Intended use or context of the media (e.g., 'profile picture', 'event banner').
            Nullable if not specified.
        upload_date (datetime):
            Timestamp when the media was uploaded. Required.
        sharing_status (str):
            Current sharing status of the media (e.g., 'public', 'private', 'restricted').
            Required.
        id_user (int):
            Foreign key referencing the user who uploaded the media (app_user.id_user).
            Required.
        id_event (Optional[int]):
            Foreign key referencing the event associated with the media (event.id_event).
            Nullable if the media is not linked to an event.
        id_location (Optional[int]):
            Foreign key referencing the location associated with the media (location.id_location).
            Nullable if the media is not linked to a location.
        location (List['LocationDB']):
            Many-to-one relationship with LocationDB. Represents the location(s)
            associated with this media.
        user (List['UserDB']):
            Many-to-one relationship with UserDB. Represents the user(s)
            who uploaded or own this media.
        event (List['EventDB']):
            Many-to-one relationship with EventDB. Represents the event(s)
            associated with this media.
    """
    
    __tablename__ = 'media'

    #region Column

    id_media: Mapped[int] = mapped_column(
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

    label: Mapped[str] = mapped_column(
        Text
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text
    )

    format_media: Mapped[str] = mapped_column(
        Text
    )

    url: Mapped[str] = mapped_column(
        Text
    )

    usage_media: Mapped[Optional[str]] = mapped_column(
        Text
    )

    upload_date: Mapped[datetime.datetime] = mapped_column(
        DateTime
    )

    sharing_status: Mapped[str] = mapped_column(
        Text
    )

    id_user: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('app_user.id_user', ondelete="CASCADE"),
    )

    id_event: Optional[Mapped[int]] = mapped_column(
        BigInteger,
        ForeignKey('event.id_event'),
    )

    id_location: Optional[Mapped[int]] = mapped_column(
        BigInteger,
        ForeignKey('location.id_location')
    )

    #endregion

    #region Relationship

    location: Mapped[list['LocationDB']] = relationship(
        'LocationDB',
        back_populates='media'
    )

    user: Mapped[list['UserDB']] = relationship(
        'UserDB',
        back_populates='media'
    )

    event: Mapped[list['EventDB']] = relationship(
        'EventDB',
        back_populates='media'
    )

    #endregion
