from fastapi import APIRouter, Depends, HTTPException
from schema.organizer import (
    CreateOrganizer,
    ResponseOrganizer,
    UpdateOrganizer
)
from schema.organizer_dashboard import DashboardStat
from model.organizer import OrganizerDB
from service.organizer import create_organizer_password, delete_organizer_db, update_organizer_db
from core.dependencies import OrganizerDependency, SessionDependency
from starlette.responses import Response
from service.organizer_stat import get_full_stats

router = APIRouter(
    prefix="/organizers",
    tags=["Organizers"]
)

@router.get("/", response_model=list[ResponseOrganizer])
async def get_organizers(db: SessionDependency):
    organizers = db.query(OrganizerDB).all()
    return organizers


@router.get("/dashboard", response_model=DashboardStat)
async def get_dashboard(
    db: SessionDependency,
    organizer: OrganizerDependency
):
    """Récupère les statistiques pour l'organisateur connecté."""
    return get_full_stats(db,organizer.id_user)


@router.get("/{organizer_id}", response_model=ResponseOrganizer)
async def get_organizer(organizer_id: int, db: SessionDependency) -> ResponseOrganizer:
    """Route to get an organizer by ID.

    Args:
        organizer_id (int): The ID of the organizer to retrieve
        db (SessionDependency): The database session

    Returns:
        OrganizerSchema: The retrieved organizer object
    """
    organizer = db.query(OrganizerDB).filter(OrganizerDB.id_organizer == organizer_id).first()
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")
    return organizer

@router.post("/", response_model=ResponseOrganizer)
async def create_organizer_req(organizer: CreateOrganizer, db: SessionDependency) -> ResponseOrganizer:
    """Route to create an organizer.

    Args:
        organizer (CreateOrganizer): The organizer data for creation
        db (SessionDependency): The database session

    Returns:
        OrganizerSchema: The created organizer object
    """
    if organizer.auth_type == 'password':
        new_organizer = create_organizer_password(
            organizer.username,
            organizer.email,
            organizer.siret,
            organizer.description,
            organizer.token,
            db
        )
    if organizer.auth_type == 'google':
        raise HTTPException(status_code=400, detail="Google authentication not implemented yet")
    if organizer.auth_type == 'facebook':
        raise HTTPException(status_code=400, detail="Facebook authentication not implemented yet")
    return new_organizer
    
@router.put("/")
async def update_organizer(new_organizer: UpdateOrganizer, organizer: OrganizerDependency, db: SessionDependency):
    update_organizer_db(new_organizer= new_organizer, organizer_id= organizer.id_user, db= db)
    return Response(status_code=201, content="Update success")

@router.delete("/{organizer_id}")
async def delete_organizer(organizer_id: int, db : SessionDependency):
    delete_organizer_db(id_organizer= organizer_id, db= db)
    return Response(status_code=200, content="Delete Success")