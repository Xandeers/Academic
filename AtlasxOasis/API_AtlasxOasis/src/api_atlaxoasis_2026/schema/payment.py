from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic.config import ConfigDict

class PaymentSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_payment : int
    id_user : int
    price: Decimal
    status_amount : Optional[str]
    status_payment : Optional[str]
    date_payment : datetime
    method_payment : Optional[str]