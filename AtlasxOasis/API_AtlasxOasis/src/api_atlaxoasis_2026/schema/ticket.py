from pydantic import BaseModel
from typing import Optional
from pydantic.config import ConfigDict

class TicketSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_ticket : int
    id_ticket_type : int
    status_ticket : Optional[str]
    ticket_type_event: Optional[str]
