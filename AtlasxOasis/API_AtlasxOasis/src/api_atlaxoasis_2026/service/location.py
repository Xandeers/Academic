from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing_extensions import Optional
from decimal import Decimal
from model.location import LocationDB


def create_location_db(
    name : Optional[str],
    address : Optional[str],
    city : Optional[str],
    postal_code : Optional[str],
    longitude : Optional[Decimal],
    latitude : Optional[Decimal],
    nearby_transport : Optional[str],
    max_capacity: Optional[int],
    accessibility : Optional[bool],
    db : Session
):
    new_location = LocationDB(
        max_capacity = max_capacity,
        name = name,
        address = address,
        city = city,
        postal_code = postal_code,
        longitude = longitude,
        latitude = latitude,
        nearby_transport = nearby_transport,
        accessibility = accessibility
    )
    
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    
    return new_location

def delete_location_db(id_location: int, db: Session):
    location = db.query(LocationDB).filter(LocationDB.id_location == id_location).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(location)
    db.commit()
    