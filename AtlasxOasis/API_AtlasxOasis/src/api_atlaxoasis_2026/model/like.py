from sqlalchemy import (
    BigInteger, 
    DateTime, 
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from datetime import datetime
from core.base import Base

class LikeDB(Base):
    __tablename__ =  "like_customer"

    #region Column

    id_customer : Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("customer.id_customer", ondelete="CASCADE"), 
        primary_key=True,
        nullable=False
    )

    id_event : Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("event.id_event", ondelete="CASCADE"), 
        primary_key=True,
        nullable=False
    )

    date_like: Mapped[datetime] = mapped_column(
        DateTime
    )

    #endregion

    #region Relationship

    customer: Mapped["CustomerDB"] = relationship(
        "CustomerDB",
        back_populates="like"
    )

    event: Mapped["EventDB"] = relationship(
        "EventDB",
        back_populates="like"
    )

    #endregion
