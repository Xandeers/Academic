from core.dependencies import CustomerDependency
from fastapi import APIRouter
from model.like import LikeDB
from routes.ticket_type_event import SessionDependency
from schema.like import ResponseLikeCustomer

router = APIRouter(
    prefix= "/like",
    tags=["Like"]
)

@router.get("/", response_model= list[ResponseLikeCustomer])
async def get_like(customer: CustomerDependency, db: SessionDependency):
    likes = db.query(LikeDB).filter(LikeDB.id_customer == customer.id_user).all()
    return likes