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


class UserDB(Base):
    """
    SQLAlchemy model representing a user in the application.

    This class defines the core attributes of a user, including their type, name, email,
    and an optional description. It also establishes relationships with media, authentication,
    payments, and follow relationships.

    Attributes:
        id_user (int):
            Primary key. Auto-incremented unique identifier for the user.
            Required (nullable=False).
        type_user (str):
            Type of user (e.g., 'standard', 'premium', 'admin', 'guest').
        name (str):
            Full name of the user. Required.
        email (str):
            Email address of the user. Required.
        description (Optional[str]):
            Optional description or bio of the user.
        media (List[MediaDB]):
            One-to-many relationship with MediaDB. Represents all media (images, videos)
            uploaded or associated with this user.
        authentication (List[AuthenticationDB]):
            One-to-many relationship with AuthenticationDB. Represents all authentication
            records (e.g., login sessions, security tokens) linked to this user.
        payment (List[PaymentDB]):
            One-to-many relationship with PaymentDB. Represents all payment transactions
            made by this user.
        followed_by (List[FollowDB]):
            One-to-many relationship with FollowDB. Represents all users who follow
            this user (in a social context).
    """
    
    __tablename__ =  "app_user"

    #region Column

    id_user : Mapped[int] = mapped_column(
        BigInteger, 
        Identity(
            always = True, 
            start = 1, 
            increment = 1, 
            minvalue = 1, 
            maxvalue = 9223372036854775807, 
            cycle = False,
            cache = 1
        ),
        primary_key=True,
        nullable=False
    )

    type_user : Mapped[str] = mapped_column(
        Text
    )

    username : Mapped[str] = mapped_column(
        Text
    )

    email : Mapped[str] = mapped_column(
        Text,
        unique=True
    )

    description : Mapped[Optional[str]] = mapped_column(
        Text
    )

    #endregion

    __mapper_args__ = {
        "polymorphic_on": type_user,
    }

    #region Relationship

    media: Mapped[list['MediaDB']] = relationship(
        'MediaDB',
        back_populates = 'user',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    authentication: Mapped[list['AuthenticationDB']] = relationship(
        'AuthenticationDB', 
        back_populates = 'user',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    payment: Mapped[list['PaymentDB']] = relationship(
        'PaymentDB',
        back_populates = 'user'
    )

    followed_by: Mapped[list['FollowDB']] = relationship(
        'FollowDB', 
        back_populates = 'followed_user',
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    #endregion
