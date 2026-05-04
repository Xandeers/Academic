from pydantic import BaseModel, Field
from typing import Optional


class BookingSchema(BaseModel):
    
    id_ticket_type : int 
    quantity : int = Field(default=1, ge=1)



class BookingResumeSchema(BaseModel):

    id_event :int
    id_ticket_type: int 
    quantity :int = Field(default=1 , ge=1)
    status_ticket : Optional[str]