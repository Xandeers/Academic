from core.dependencies import SessionDependency
from fastapi import APIRouter, Response
from model.promotion import PromotionDB
from schema.promotion import CreatePromotion, ResponsePromotion
from service.promotion import create_promotion_db, delete_promotion_db

router = APIRouter(
    prefix="/promotions",
    tags=["Promotions"]
)

@router.get("/", response_model= list[ResponsePromotion])
async def get_all_promotions(db: SessionDependency):
    promotions = db.query(PromotionDB).all()
    return promotions
    
@router.post("/")
async def create_promotion(promotion : CreatePromotion, db: SessionDependency):
    new_promotion = create_promotion_db(
        id_promotion_type= promotion.id_promotion_type,
        start_date= promotion.start_date,
        end_date= promotion.end_date,
        status_promotion= promotion.status_promotion,
        type_promotion= promotion.type_promotion,
        description= promotion.description,
        db= db
    )
    
@router.delete("/{promotion_id}")
async def delete_promotion(promotion_id: int, db: SessionDependency):
    delete_promotion_db(id_promotion=promotion_id, db=db)
    return Response(status_code=200, content="Delete success")
    