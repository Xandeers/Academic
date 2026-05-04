
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing_extensions import Optional
from model.media import MediaDB


def create_media_db(
    label : str,
    description : Optional[str],
    format_media : str,
    url : str,
    usage_media : str,
    upload_date : datetime,
    sharing_status : str,
    id_user : int,
    id_event : Optional[int],
    id_location: Optional[int],
    db : Session
):
    new_media = MediaDB(
        label= label,
        description= description,
        format_media= format_media,
        url= url,
        usage_media= usage_media,
        upload_date= upload_date,
        sharing_status= sharing_status,
        id_user= id_user,
        id_event= id_event,
        id_location = id_location
    )
    
    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    
    return new_media

def delete_media_db(id_media: int, db : Session):
    media = db.query(MediaDB).filter(MediaDB.id_media == id_media).first()
    if media is None:
        raise HTTPException(status_code=404, detail="Media not found")
    db.delete(media)
    db.commit()