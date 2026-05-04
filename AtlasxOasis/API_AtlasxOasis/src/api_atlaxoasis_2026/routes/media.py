from fastapi import APIRouter, Response
from core.dependencies import (
    SessionDependency,
    CurrentUserDependency
)
from model.media import MediaDB
from schema.media import (
    ResponseMedia,
    CreateMedia
)
from service.media import create_media_db, delete_media_db

router = APIRouter(
    prefix="/media",
    tags=["Media"]
)

@router.get("/", response_model= list[ResponseMedia])
async def get_all_media(db: SessionDependency):
    medias = db.query(MediaDB).all()
    return medias
    
@router.post("/")
async def create_media(media: CreateMedia, user : CurrentUserDependency, db: SessionDependency):
    new_media = create_media_db(
        label= media.label,
        description= media.description,
        format_media= media.format_media,
        url= media.url,
        usage_media= media.usage_media,
        upload_date= media.upload_date,
        sharing_status= media.sharing_status,
        id_user= user.id_user,
        id_event= media.id_event,
        id_location= media.id_location,
        db= db
    )
    return new_media
    
@router.delete("/{media_id}")
async def delete_media(media_id: int, db: SessionDependency):
    delete_media_db(id_media=media_id, db= db)
    return Response(status_code=200, content="Delete success")