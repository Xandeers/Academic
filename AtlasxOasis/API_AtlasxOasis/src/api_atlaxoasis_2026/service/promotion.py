from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from model.promotion import PromotionDB
from sqlalchemy.orm import Session


def create_promotion_db(
    id_promotion_type : int,
    start_date : datetime,
    end_date : datetime,
    status_promotion : str,
    type_promotion : str,
    description : Optional[str],
    db : Session
):
    new_promotion = PromotionDB(
        id_promotion_type = id_promotion_type,
        start_date = start_date,
        end_date = end_date,
        status_promotion = status_promotion,
        type_promotion = type_promotion,
        description= description,
    )
    
    db.add(new_promotion)
    db.commit()
    db.refresh(new_promotion)
    
    return new_promotion
    
def delete_promotion_db(id_promotion: int, db: Session):
    promotion = db.query(PromotionDB).filter(PromotionDB.id_promotion == id_promotion).first()
    if promotion is None:
        raise HTTPException(status_code=404, detail="Promotion not found")
    db.delete(promotion)
    db.commit()