from pydantic import BaseModel
from pydantic.config import ConfigDict

class CategorySchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )

    id_category : int
    label : str

class CreateCategory(BaseModel):
    
    label: str

class CategoryResponse(BaseModel):
    
    id_category: int
    label: str
