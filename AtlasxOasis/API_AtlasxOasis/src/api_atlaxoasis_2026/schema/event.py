from pydantic import (
    BaseModel, 
    Field, 
    computed_field, 
    ConfigDict
)
from datetime import datetime
from typing import (
    Any, 
    Optional,
    Literal
)
from pydantic.functional_serializers import field_serializer
from schema.organizer import OrganizerSchema

from model.category import CategoryDB
from model.organizer import OrganizerDB
from model.location import LocationDB
from model.media import MediaDB
from model.ticket_type_event import TicketTypeEventDB
from model.like import LikeDB
from model.promotion import PromotionDB

# =============================================================================
# PATTERN : Pydantic Schema with SQLAlchemy relationships
# =============================================================================
#
# PROBLEM : Pydantic cannot serialize SQLAlchemy objects directly.
#
# SOLUTION :
#   1. "_raw" field  → receives the raw SQLAlchemy object (excluded from JSON)
#                      via `validation_alias` which maps the SQLAlchemy relation name
#   2. computed_field → transforms _raw into primitive types (int, dict, str...)
#                       and appears in the JSON response
#
# EXAMPLE :
#   SQLAlchemy :  event.like        → [LikeDB, LikeDB, ...]
#   _raw field :  like_raw          → receives [LikeDB, ...], excluded from JSON
#   computed :    like              → returns [{"customer_id": 1}, ...], in JSON
#
# =============================================================================

class EventSchema(BaseModel):

    model_config= ConfigDict(
        from_attributes=True
    )

    id_event : int
    id_organizer : int
    name: str
    start_date : datetime
    end_date : datetime
    creation_date : datetime
    event_status : str
    max_capacity : Optional[int]
    description : Optional[str]
    metadata : Optional[dict[str, Any]]

class ResponseEventSchema(BaseModel):

    model_config= ConfigDict(
        arbitrary_types_allowed=True, # Allows using types that Pydantic doesn’t know how to handle natively (enables better typing)
        from_attributes=True, # Enables serialization/deserialization from ORM classes
    )

    #region Simple fields
    # -------------------------------------------------------------------------
    # Simple fields — mapped directly from SQLAlchemy
    # -------------------------------------------------------------------------

    id_event : int
    # validation_alias="name" because the SQLAlchemy attribute is "name"
    title : str = Field(
        validation_alias="name"
    )
    description : Optional[str] = None

    status : str = Field(
        validation_alias="event_status"
    )
    begin_date : datetime = Field(
        validation_alias="start_date"
    )
    end_date : datetime

    capacity : Optional[int] = Field(
        default=None,
        validation_alias="max_capacity"
    )

    createdAt : datetime = Field(
        validation_alias='creation_date'
    )

    tag : Optional[list[str]] = None

    #endregion
    #region Raw fields
    # -------------------------------------------------------------------------
    # RAW fields — receive raw SQLAlchemy objects
    #
    # Rules :
    #   - exclude=True         → never serialized in the JSON response
    #   - validation_alias     → exact name of the relation in the SQLAlchemy model
    #   - default=[]           → prevents errors if the relation is not loaded
    # -------------------------------------------------------------------------
    category_raw : list[CategoryDB] = Field(
        default=[], 
        exclude=True,
        validation_alias="category"
    )

    organizer_owner_raw : Optional[OrganizerDB] = Field(
        default=None, 
        exclude=True,
        validation_alias="organizer_owner"
    )

    location_raw : list[LocationDB] = Field(
        default=[],
        exclude=True,
        validation_alias='location'
    )

    media_raw : list[MediaDB] = Field(
        default=[],
        exclude=True,
        validation_alias="media"
    )

    ticket_type_event_raw : list[TicketTypeEventDB] = Field(
        default=[],
        exclude=True,
        validation_alias="ticket_type_event"
    )

    like_raw : list[LikeDB] = Field(
        default=[], 
        exclude=True,
        validation_alias="like"
    )

    promotion_raw : list[PromotionDB] = Field(
        default=[],
        exclude=True,
        validation_alias='promotion'
    )
    
    # Converts datetime objects to ISO format strings when serializing to JSON
    @field_serializer("begin_date", "end_date", "createdAt")
    def serialize_datetime(self, value: datetime):
        return value.isoformat()

    #endregion
    #region Computed Field
    # -------------------------------------------------------------------------
    # Computed fields — transform _raw into primitive types for the JSON response
    #
    # Rules :
    #   - Always return primitive types or Schema only (int, str, dict, list, EventSchema)
    #   - Don't return a Schema with other computed field (avoid infinite loop)
    #   - Never return a SQLAlchemy object
    # -------------------------------------------------------------------------
    
    @computed_field
    @property
    def category(self) -> list[dict[str, int | str]]:
        return [
            {
                "category_id" : category.id_category,
                "name" : category.label
            } for category in self.category_raw
        ]
    
    @computed_field
    @property
    def location_id(self) -> list[dict[str, int | str | None]]:
        return [
            {
                "location_id" : location.id_location,
                "name" : location.name
            } for location in self.location_raw
        ]
    
    @computed_field
    @property
    def image(self) -> list[dict[str, int | str | None]]:
        return [
            {
                "media_id" : media.id_media,
                "media_usage" : media.usage_media,
                "media_fromat" : media.format_media,
                "media_url" : media.url
            } for media in self.media_raw
        ]
    
    @computed_field
    @property
    def price(self) -> float:
        ticket_price_list = [
            ticket_type.price 
            for ticket_type in self.ticket_type_event_raw 
            if ticket_type.price is not None
        ] 
        return float(min(ticket_price_list)) if ticket_price_list else 0
    
    @computed_field
    @property
    def reserved(self) -> int:
        nb_ticket_sell_list = [len(ticket_type.ticket) for ticket_type in self.ticket_type_event_raw]
        return sum(nb_ticket_sell_list)
    
    @computed_field
    @property
    def organizer(self) -> OrganizerSchema:
        return OrganizerSchema.model_validate(self.organizer_owner_raw)
    
    @computed_field
    @property
    def like_count(self) -> int:
        return len(self.like_raw)
    
    @computed_field
    @property
    def is_featured(self) -> bool:
        return self.promotion_raw != []
    
    #endregion

class CreateEventSchema(BaseModel):
    name: str
    start_date : datetime
    end_date : datetime
    created_date: datetime
    event_status : Literal['published', 'finish', 'not_publish']
    max_capacity : Optional[int]
    description : Optional[str]
    metadata : Optional[dict[str, Any]]

class UpdateEventSchema(BaseModel):
    name: Optional[str] = None
    start_date : Optional[datetime] = None
    end_date : Optional[datetime] = None
    event_status : Optional[Literal['published', 'finish', 'not_publish']] = None
    max_capacity : Optional[int] = None
    description : Optional[str] = None
    metadata : Optional[dict[str, Any]] = None