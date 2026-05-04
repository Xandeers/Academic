from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic.config import ConfigDict

class MediaSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_media : int
    label : str
    description : Optional[str] = None
    format_media : str
    url : str
    usage_media : str
    upload_date : datetime
    sharing_status : str
    id_user : int
    id_event : Optional[int] = None
    id_location : Optional[int] = None
    
class ResponseMedia(MediaSchema):
    pass
    
class CreateMedia(BaseModel):
    label : str
    description : Optional[str] = None
    format_media : str
    url : str
    usage_media : str
    upload_date : datetime
    sharing_status : str
    id_event : Optional[int] = None
    id_location : Optional[int] = None

