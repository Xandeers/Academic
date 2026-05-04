from sqlalchemy import (
    BigInteger, 
    Text, 
    Identity
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from typing import Optional
from core.base import Base

class CategoryDB(Base):
    """
    Represents a category for events (e.g., "sport", "music", "conference").

    Categories are used to classify events and enable filtering/searching.
    The `label` field is optional to support hierarchical or unnamed categories.

    Attributes:
        id_category (int): Unique category identifier (auto-incremented primary key).
        label (str): Human-readable name of the category.
        event (List[EventDB]): Events associated with this category (many-to-many relationship).
    """

    __tablename__ =  "category"

    #region Column

    id_category : Mapped[int] = mapped_column(
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

    label : Mapped[str] = mapped_column(
        Text
    )

    #endregion

    #region Relationship

    event: Mapped[list['EventDB']] = relationship(
        'EventDB', 
        secondary = 'event_category', 
        back_populates = 'category'
    )

    #endregion
