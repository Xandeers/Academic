from sqlalchemy import (
    BigInteger, 
    Text,
    ForeignKey 
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from core.base import Base

class AuthenticationDB(Base):
    """
    Represents an authentication method linked to a user.

    This table stores authentication tokens (e.g., API keys, JWT, OAuth tokens)
    and their types (e.g., "google", "github", "password_reset").

    Attributes:
        type_auth (str): Type of authentication (primary key).
        id_user (int): Associated user ID (primary and foreign key).
        token (str): Authentication or session token.
        user (UserDB): User who owns this authentication (one-to-many relationship).
    """

    __tablename__ = "authentication"

    #region Column

    type_auth : Mapped[str] = mapped_column(
        Text, 
        primary_key=True
    )

    id_user: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('app_user.id_user', ondelete="CASCADE"),
        primary_key=True
    )

    token: Mapped[str] = mapped_column(
        Text
    )

    #endregion

    #region Relationship

    user : Mapped['UserDB'] = relationship(
        'UserDB',
        back_populates  = 'authentication'
    )    
    
    #endregion
