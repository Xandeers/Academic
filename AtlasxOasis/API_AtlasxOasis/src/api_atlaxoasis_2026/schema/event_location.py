from pydantic import BaseModel
from pydantic.config import ConfigDict

class EventLocationSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_location : int
    id_event : str
