from sqlalchemy import (
    BigInteger,  
    Text, 
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from typing import Optional
from datetime import datetime
from core.base import Base

class FollowDB(Base):
    """
    Represents a "follow" relationship between a customer and another user (e.g., organizer, artist).

    Attributes:
        id_follower_customer (int): Foreign key referencing the customer (primary key).
        id_followed_user (int): Foreign key referencing the followed user (primary key).
        date_follow (Optional[datetime]): Date and time when the follow was created.
        status_follow (Optional[str]): Status of the follow (e.g., "active", "pending", "blocked").
        followed_user (UserDB): The user being followed (many-to-one).
        follower_customer (CustomerDB): The customer who is following (many-to-one).
    """

    __tablename__ = "follow"

    #region Column

    id_follower_customer: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('customer.id_customer', ondelete="CASCADE"), 
        primary_key=True
    )

    id_followed_user: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('app_user.id_user', ondelete="CASCADE"),
        primary_key=True
    )

    date_follow: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime
    )

    status_follow: Mapped[Optional[str]] = mapped_column(
        Text
    )

    #endregion

    #region Relationship

    followed_user: Mapped['UserDB'] = relationship(
        'UserDB', 
        back_populates='followed_by',
        foreign_keys=[id_followed_user]
    )

    follower_customer: Mapped['CustomerDB'] = relationship(
        'CustomerDB', 
        back_populates='follow',
        foreign_keys=[id_follower_customer]
    )

    #endregion
