from fastapi import (
    APIRouter,
    HTTPException,
)
from core.dependencies import SessionDependency
from fastapi.responses import Response
from schema.category import(
    CategoryResponse,
    CreateCategory
)
from model.category import CategoryDB
from service.category import create_category_db, delete_category_db


router = APIRouter(
    prefix="/category",
    tags=["Category"]
)

@router.get('/', response_model=list[CategoryResponse])
async def get_category(db: SessionDependency) -> list[CategoryResponse]:
    category = db.query(CategoryDB).all()
    return category

@router.get('/{category_id}', response_model=CategoryResponse)
async def get_category_by_id(category_id: int, db:SessionDependency) -> CategoryResponse:
    category = (db.query(CategoryDB)
        .filter(CategoryDB.id_category == category_id)
        .first()
    )
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post('/')
async def create_category(category: CreateCategory, db:SessionDependency):
    new_category = create_category_db(label=category.label, db=db)
    return new_category
    
@router.delete('/{category_id}')
async def delete_category(category_id: int, db:SessionDependency):
    delete_category_db(id_category= category_id, db= db)
    return Response(status_code=200, content="Delete success")
