from sqlalchemy import (
    BigInteger, 
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
)
from core.base import Base

class PromotionEventDB(Base):
    """
    SQLAlchemy association model representing the many-to-many relationship
    between sale objects and events for promotional purposes.

    This class serves as a junction table to link sale objects (e.g., tickets, products)
    to events they are promoting or associated with, without additional attributes.

    Attributes:
        id_sale_object (int):
            Composite primary key. Foreign key referencing the sale object (sale_object.id_sale_object).
        id_event (int):
            Composite primary key. Foreign key referencing the event (event.id_event).
    """
    
    __tablename__ = 'promotion_event'

    #region Column

    id_promotion: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('promotion.id_promotion'),
        primary_key=True
    )

    id_event: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey('event.id_event'),
        primary_key=True
    )

    #endregion
