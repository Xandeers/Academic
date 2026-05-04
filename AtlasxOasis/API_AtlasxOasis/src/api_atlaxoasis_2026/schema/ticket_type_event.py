from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from pydantic.config import ConfigDict

class TicketTypeEventSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_ticket_type : int
    id_event : int
    price : Optional[Decimal] = None
    label : Optional[str] = None
    description : Optional[str] = None
    quantity : Optional[int] = None

class TicketTypeEventUpdateSchema(BaseModel):

    price: Optional[Decimal] = None
    label: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)