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
from model.user import UserDB

class OrganizerDB(UserDB):
    """
    SQLAlchemy model representing an organizer, inheriting from UserDB.

    Extends the base user model with organizer-specific attributes and relationships.
    This class is used to represent users who have the role of event organizers,
    with additional business-related information such as SIRET number.

    Attributes:
        id_organizer (int):
            Primary key. Foreign key referencing the base user (app_user.id_user).
            Inherits all user attributes from UserDB.
        siret (Optional[str]):
            SIRET number for professional organizers. Nullable if the organizer
            is not a registered business entity.
        event_create (List[EventDB]):
            One-to-many relationship with EventDB. Represents all events created/owned
            by this organizer.
        organizer_event (List[OrganizerEventDB]):
            One-to-many relationship with OrganizerEventDB. Represents all events
            where this organizer has a role (through the association table).
    """
    
    __tablename__ = 'organizer'

    #region Column

    id_organizer: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("app_user.id_user"),
        primary_key=True
    )

    siret: Mapped[Optional[str]] = mapped_column(
        Text
    )

    #endregion

    __mapper_args__ = {
        "polymorphic_identity": "organizer",
    }

    #region Relationship

    event_create: Mapped[list['EventDB']] = relationship(
        'EventDB',
        back_populates='organizer_owner',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    organizer_event: Mapped[list['OrganizerEventDB']] = relationship(
        'OrganizerEventDB', 
        back_populates='organizer'
    )

    #endregion
