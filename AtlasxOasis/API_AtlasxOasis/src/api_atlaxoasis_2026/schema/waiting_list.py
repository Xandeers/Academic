from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic.config import ConfigDict

class WaitingListSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
    id_customer : int
    id_event : int
    added_date : datetime
    status_waiting : Optional[str]
    type_priority : Optional[str]
