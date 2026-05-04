from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from pydantic.config import ConfigDict

class PromotionTypeSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
    id_promotion_type : int
    name : str
    description : Optional[str] = None
    price : Optional[Decimal] = None
