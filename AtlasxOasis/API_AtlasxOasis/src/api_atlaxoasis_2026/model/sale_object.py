from sqlalchemy import (
    BigInteger,  
    Text,  
    ForeignKey, 
    Identity
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from typing import Optional
from core.base import Base

class SaleObjectDB(Base):
    """
    SQLAlchemy model representing a sale object in the system.

    This class defines items that can be purchased, such as tickets, products, or services.
    Each sale object is linked to a payment transaction.

    Attributes:
        id_sale_object (int):
            Primary key. Auto-incremented unique identifier for the sale object.
            Also serves as a foreign key referencing the associated payment (payment.id_payment).
        id_payment (Optional[int]):
            Redundant reference to the payment ID for direct access.
            Nullable if the sale object is not yet associated with a payment.
        type_object (Optional[str]):
            Type of the sale object (e.g., 'ticket', 'product', 'service', 'subscription').
            Nullable if not specified.
        payment (Optional[PaymentDB]):
            Many-to-one relationship with PaymentDB. Represents the payment transaction
            associated with this sale object. Nullable if not yet linked to a payment.
    """
    
    __tablename__ = 'sale_object'

    #region Column

    id_sale_object: Mapped[int] = mapped_column(
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
        ForeignKey('payment.id_payment'), 
        primary_key=True
    )

    id_payment: Mapped[Optional[int]] = mapped_column(
        BigInteger
    )

    type_object: Mapped[Optional[str]] = mapped_column(
        Text
    )

    #endregion

    __mapper_args__ = {
        "polymorphic_on": type_object,
    }

    #region Relationship

    payment: Mapped[Optional['PaymentDB']] = relationship(
        'PaymentDB', 
        back_populates='sale_object'
    )

    #endregion
