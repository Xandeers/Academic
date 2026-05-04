from fastapi import APIRouter, Response
from core.dependencies import SessionDependency
from model.location import LocationDB
from schema.location import (
    ResponseLocation,
    CreateLocation
)
from service.location import create_location_db, delete_location_db

router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)

@router.get("/", response_model=list[ResponseLocation])
async def get_all(db: SessionDependency):
    locations = db.query(LocationDB).all()
    return locations
    
@router.post("/")
async def create_location(location : CreateLocation, db: SessionDependency):
    new_location = create_location_db(
        max_capacity= location.max_capacity,
        name= location.name,
        address= location.address,
        city= location.city,
        postal_code= location.postal_code,
        longitude= location.longitude,
        latitude= location.latitude,
        nearby_transport= location.nearby_transport,
        accessibility= location.accessibility,
        db= db
    )
    
    return new_location

@router.delete("/{location_id}")
async def delete_location(location_id: int, db: SessionDependency):
    delete_location_db(id_location=location_id, db=db)
    return Response(status_code=200, content="Delete success")