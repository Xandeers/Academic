from datetime import datetime
from model.follow import FollowDB
from sqlalchemy.orm import Session
from typing_extensions import Optional


def create_follow(
    id_follower_customer: int, 
    id_followed_user: int,
    status_follow : Optional[str],
    db: Session
):
    new_follow = FollowDB(
        id_follower_customer= id_follower_customer,
        id_followed_user = id_followed_user,
        date_follow= datetime.now(),
        status_follow= status_follow
    )
    
    db.add(new_follow)
    db.commit()
    
def delete_follow(
    id_follower_customer: int, 
    id_followed_user: int,
    db: Session
):
    follow = (db.query(FollowDB)
        .filter(FollowDB.id_followed_user == id_followed_user and
            FollowDB.id_follower_customer == id_follower_customer
        ).first()
    )
    if follow is None:
        raise ValueError("Follow not found")
    db.delete(follow)
    db.commit()
    
    