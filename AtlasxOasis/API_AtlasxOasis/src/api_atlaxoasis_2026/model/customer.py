from sqlalchemy import (
    BigInteger, 
    ForeignKey,
    Text
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from model.user import UserDB

class CustomerDB(UserDB):
    """
    Extends UserDB to represent a customer in the system.

    Inherits all attributes from UserDB and adds customer-specific relationships,
    such as waiting lists and follow relationships.

    Attributes:
        id_customer (int): Primary key, linked to the inherited user ID (foreign key to app_user.id_user).
        waiting_list (List[WaitingListDB]): Events the customer is waitlisted for.
        follow (List[FollowDB]): Entities (organizers, customers) the customer follows.
    """
    
    __tablename__ = "customer"

    #region Column

    id_customer : Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("app_user.id_user"),
        primary_key=True,
    )

    firstname : Mapped[str] = mapped_column(
        Text
    )

    lastname : Mapped[str] = mapped_column(
        Text
    )

    #endregion

    __mapper_args__ = {
        "polymorphic_identity": "customer",
    }

    #region Relationship

    waiting_list : Mapped[list['WaitingListDB']] = relationship(
        'WaitingListDB', 
        back_populates='customer'
    )

    follow : Mapped[list['FollowDB']] = relationship(
        "FollowDB",
        back_populates="follower_customer",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    like: Mapped[list['LikeDB']] = relationship(
        'LikeDB',
        back_populates='customer'
    )

    #endregion
