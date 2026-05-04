from sqlalchemy import (
    BigInteger, 
    Text, 
    DateTime, 
    ForeignKey, 
    Identity,
    Numeric
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from typing import Optional
from datetime import datetime
from decimal import Decimal
from core.base import Base

class PaymentDB(Base):
    """
    SQLAlchemy model representing a payment transaction in the system.

    This class stores financial transaction details, including amount, status,
    payment method, and associations with users and sale objects.

    Attributes:
        id_payment (int):
            Primary key. Auto-incremented unique identifier for the payment.
        id_user (int):
            Foreign key referencing the user who made the payment (app_user.id_user).
            Required (nullable=False).
        price (Optional[Decimal]):
            Amount of the payment, stored with precision of 10 digits (2 decimal places).
            Nullable if the amount is not yet determined.
        status_montant (Optional[str]):
            Status of the amount (e.g., 'pending', 'confirmed', 'refunded').
            Nullable if not yet defined.
        status_payment (Optional[str]):
            Status of the payment process (e.g., 'initiated', 'completed', 'failed').
            Nullable if not yet processed.
        date_payment (Optional[datetime]):
            Timestamp when the payment was processed. Nullable if not yet recorded.
        methode_payment (Optional[str]):
            Payment method used (e.g., 'credit_card', 'paypal', 'bank_transfer').
            Nullable if not yet specified.
        user (UserDB):
            Many-to-one relationship with UserDB. Represents the user associated
            with this payment.
        sale_object (List[SaleObjectDB]):
            One-to-many relationship with SaleObjectDB. Represents all sale objects
            (e.g., tickets, products) linked to this payment.
    """

    __tablename__ = 'payment'

    #region Column

    id_payment: Mapped[int] = mapped_column(
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

    id_user: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("app_user.id_user"),
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    status_amount: Mapped[Optional[str]] = mapped_column(
        Text
    )

    status_payment: Mapped[Optional[str]] = mapped_column(
        Text
    )

    date_payment: Mapped[datetime.datetime] = mapped_column(
        DateTime
    )

    methode_payment: Mapped[Optional[str]] = mapped_column(
        Text
    )

    #endregion

    #region Relationship

    user: Mapped['UserDB'] = relationship(
        'UserDB', 
        back_populates='payment'
    )

    sale_object: Mapped[list['SaleObjectDB']] = relationship(
        'SaleObjectDB',
        back_populates='payment'
    )

    #endregion

