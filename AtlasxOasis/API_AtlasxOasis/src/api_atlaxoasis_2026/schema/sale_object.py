from pydantic import BaseModel
from pydantic.config import ConfigDict

class SaleObjectSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_sale_object : int
    id_payment : int
    type_object : str
