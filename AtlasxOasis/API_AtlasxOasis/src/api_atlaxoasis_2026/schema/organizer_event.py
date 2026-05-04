from pydantic import BaseModel
from typing import Optional
from pydantic.config import ConfigDict

class OrganizerEventSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_organizer : int
    id_event : int
    role : Optional[str] = None
