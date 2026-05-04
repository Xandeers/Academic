from sqlalchemy import (
    BigInteger, 
    ForeignKey ,
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column
)
from core.base import Base

class EventCategoryDB(Base):
    """
    Association table linking events to their categories.

    This table implements a many-to-many relationship between EventDB and CategoryDB.
    Each row represents a single event belonging to a single category.

    Attributes:
        id_category (int): Foreign key to the category (primary key).
        id_event (int): Foreign key to the event (primary key).
    """
    
    __tablename__ =  "event_category"

    #region Column

    id_category : Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("category.id_category"), 
        primary_key=True
    )

    id_event : Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("event.id_event"), 
        primary_key=True
    )

    #endregion
