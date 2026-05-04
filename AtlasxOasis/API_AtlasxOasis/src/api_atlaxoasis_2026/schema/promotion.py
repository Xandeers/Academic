from pydantic import BaseModel
from datetime import datetime
from pydantic.config import ConfigDict
from typing import Optional

class PromotionSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_sale_object : int
    id_promotion_type : int
    start_date : datetime
    end_date : datetime
    status_promotion : str
    type_promotion : str
    description : str

class ResponsePromotion(BaseModel):
    id_sale_object : int
    id_promotion_type : int
    start_date : datetime
    end_date : datetime
    status_promotion : str
    type_promotion : str
    description : Optional[str] = None

class CreatePromotion(BaseModel):
    id_promotion_type : int
    start_date : datetime
    end_date : datetime
    status_promotion : str
    type_promotion : str
    description : Optional[str] = None