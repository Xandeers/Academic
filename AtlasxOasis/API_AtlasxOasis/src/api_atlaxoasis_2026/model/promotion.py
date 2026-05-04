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
from model.sale_object import SaleObjectDB
from sqlalchemy.orm.properties import MappedColumn

class PromotionDB(SaleObjectDB):
    """
    SQLAlchemy model representing a promotion, inheriting from SaleObjectDB.

    Extends the base sale object model with promotion-specific attributes and relationships.
    This class represents time-limited promotional offers applied to sale objects.

    Attributes:
        id_sale_object (int):
            Primary key. Foreign key referencing the base sale object (sale_object.id_sale_object).
            Inherits all sale object attributes from SaleObjectDB.
        id_promotion_type (int):
            Foreign key referencing the promotion type (promotion_type.id_promotion_type).
            Required (nullable=False).
        start_date (Optional[datetime]):
            Start date and time of the promotion. Nullable if not yet scheduled.
        date_fin (Optional[datetime]):
            End date and time of the promotion. Nullable if no expiration is set.
        status_promotion (Optional[str]):
            Current status of the promotion (e.g., 'active', 'expired', 'pending').
            Nullable if not yet defined.
        type_promotion (Optional[str]):
            Type of promotion (e.g., 'percentage', 'fixed_amount', 'buy_one_get_one').
            Nullable if not specified.
        promotion_type (PromotionTypeDB):
            Many-to-one relationship with PromotionTypeDB. Represents the type of promotion
            applied to this sale object.
    """
    
    __tablename__ = 'promotion'

    #region Column

    id_promotion: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('sale_object.id_sale_object'), 
        primary_key=True
    )

    id_promotion_type: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey('promotion_type.id_promotion_type'),
        nullable=False
    )

    start_date: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime
    )

    end_date: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime
    )

    status_promotion: Mapped[Optional[str]] = mapped_column(
        Text
    )

    type_promotion: Mapped[Optional[str]] = mapped_column(
        Text
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text
    )

    #endregion

    __mapper_args__ = {
        "polymorphic_identity": "promotion",
    }

    #region Relationship

    promotion_type: Mapped['PromotionTypeDB'] = relationship(
        'PromotionTypeDB', 
        back_populates='promotion'
    )

    event: Mapped['EventDB'] = relationship(
        "EventDB",
        secondary='promotion_event',
        back_populates='promotion'
    )

    #endregion
