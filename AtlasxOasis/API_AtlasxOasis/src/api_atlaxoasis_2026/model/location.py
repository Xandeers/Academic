from sqlalchemy import (
    BigInteger, 
    Integer, 
    Text, 
    Numeric,
    Boolean,     
    Identity
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from typing import Optional
from decimal import Decimal
from core.base import Base

class LocationDB(Base):
    """
    SQLAlchemy model representing a location entity in the database.

    This class defines the structure and relationships for storing geographical,
    logistical, and descriptive information about a physical location.

    Attributes:
        id_location (int):
            Primary key. Auto-incremented unique identifier for the location.
            Configured with Identity to ensure sequential, non-repeating values.
        max_capacity (Optional[int]):
            Maximum capacity of the location (e.g., number of people).
            Nullable if capacity is unknown or unlimited.
        name (Optional[str]):
            Name of the location. Nullable if unnamed.
        address (Optional[str]):
            Full address of the location. Nullable if not applicable.
        city (Optional[str]):
            City where the location is located. Nullable if not specified.
        postal_code (Optional[str]):
            Postal code for the location. Nullable if not available.
        longitude (Optional[Decimal]):
            Longitude coordinate, stored with precision of 10 digits (6 decimal places).
            Nullable if coordinates are unknown.
        latitude (Optional[Decimal]):
            Latitude coordinate, stored with precision of 10 digits (6 decimal places).
            Nullable if coordinates are unknown.
        accessibility (bool):
            Boolean flag indicating whether the location is accessible to people with disabilities.
            Defaults to False if not specified.
        nearby_transport (Optional[str]):
            Description of nearby public transport options. Nullable if not provided.
        media (List['MediaDB']):
            One-to-many relationship with MediaDB. Represents all media (images, videos)
            associated with this location.
        event (List['EventDB']):
            Many-to-many relationship with EventDB via the 'event_location' association table.
            Represents all events scheduled at this location.
    """
    
    __tablename__ = "location"

    #region Column

    id_location: Mapped[int] = mapped_column(
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

    max_capacity: Mapped[Optional[int]] = mapped_column(
        Integer
    )

    name: Mapped[Optional[str]] = mapped_column(
        Text
    )

    address: Mapped[Optional[str]] = mapped_column(
        Text
    )

    city: Mapped[Optional[str]] = mapped_column(
        Text
    )

    postal_code: Mapped[Optional[str]] = mapped_column(
        Text
    )

    longitude: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 6)
    )

    latitude: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 6)
    )

    accessibility: Mapped[bool] = mapped_column(
        Boolean
    )

    nearby_transport: Mapped[Optional[str]] = mapped_column(
        Text
    )

    #endregion

    #region Relationship

    media: Mapped[list['MediaDB']] = relationship(
        'MediaDB', 
        back_populates='location'
    )

    event: Mapped[list['EventDB']] = relationship(
        'EventDB', 
        secondary='event_location', 
        back_populates='location'
    )

    #endregion