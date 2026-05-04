from pydantic import BaseModel
from pydantic.config import ConfigDict

class EventCategorySchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
    id_category : int
    id_event : str