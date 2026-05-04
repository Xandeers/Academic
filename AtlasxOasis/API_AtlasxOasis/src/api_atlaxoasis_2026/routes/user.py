from core.dependencies import CustomerDependency, SessionDependency
from fastapi import APIRouter, Response
from model.follow import FollowDB
from model.user import UserDB
from schema.follow import CreateFollow, ResponseFollowed, ResponseFollower
from schema.user import ResponseUser
from service.follow import create_follow, delete_follow

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model= list[ResponseUser])
async def get_all_users(db: SessionDependency):
    users = db.query(UserDB).all()
    return users

@router.get("/{id_user}", response_model= ResponseUser)
async def get_user(id_user: int, db: SessionDependency):
    user = db.query(UserDB).filter(UserDB.id_user == id_user).first()
    return user

@router.post("/{id_user}/follow")
async def follow_this_user(id_user: int, follow: CreateFollow , customer: CustomerDependency, db: SessionDependency):
    create_follow(
        id_followed_user=id_user, 
        id_follower_customer= customer.id_user, 
        status_follow=follow.status_follow, 
        db=db
    )
    
    return Response(status_code=201, content="Follow success")
    
@router.delete("/{id_user}/unfollow")
async def unfollow_this_user(id_user: int, customer: CustomerDependency, db: SessionDependency):
    delete_follow(
        id_follower_customer= customer.id_user,
        id_followed_user= id_user,
        db= db
    )
    return Response(status_code=200, content="Delete success")
    
@router.get("/{id_user}/followers", response_model= list[ResponseFollower])
async def get_follower(id_user: int, db: SessionDependency):
    follows = db.query(FollowDB).filter(FollowDB.id_followed_user == id_user).all()
    return follows

@router.get("/{id_user}/followed", response_model= list[ResponseFollowed])
async def get_followed(id_user: int, db: SessionDependency):
    follows = db.query(FollowDB).filter(FollowDB.id_follower_customer == id_user).all()
    return follows