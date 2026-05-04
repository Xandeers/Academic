from pydantic import BaseModel
from pydantic.config import ConfigDict

class PromotionEventSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
    id_promotion : int
    id_event : int
