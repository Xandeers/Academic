from sqlalchemy import (
    BigInteger, 
    Text, 
    Identity,
    Numeric
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from typing import Optional
from decimal import Decimal
from core.base import Base

class PromotionTypeDB(Base):
    """
    SQLAlchemy model representing a type of promotion available in the system.

    This class defines the characteristics of different promotion types that can be
    applied to sale objects or events, including their name, description, and price.

    Attributes:
        id_promotion_type (int):
            Primary key. Auto-incremented unique identifier for the promotion type.
        name (Optional[str]):
            Name of the promotion type (e.g., 'Early Bird', 'Group Discount', 'VIP Access').
            Nullable if not specified.
        description (Optional[str]):
            Detailed description of the promotion type, including terms and conditions.
            Nullable if not provided.
        price (Optional[Decimal]):
            Fixed price or discount amount associated with this promotion type.
            Stored with precision of 10 digits (2 decimal places). Nullable if the price
            is dynamic or not applicable.
        promotion (List[PromotionDB]):
            One-to-many relationship with PromotionDB. Represents all promotions
            that use this promotion type.
    """
    
    __tablename__ = 'promotion_type'

    #region Column

    id_promotion_type: Mapped[int] = mapped_column(
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

    name: Mapped[Optional[str]] = mapped_column(
        Text
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text
    )

    price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2)
    )

    #endregion

    #region Relationship

    promotion: Mapped[list['PromotionDB']] = relationship(
        'PromotionDB', 
        back_populates='promotion_type'
    )

    #endregion
