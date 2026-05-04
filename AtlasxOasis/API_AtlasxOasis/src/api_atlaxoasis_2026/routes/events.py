from fastapi import (
    APIRouter,
    HTTPException,
    Response
)
from model.event import EventDB
from schema.event import (
    ResponseEventSchema,
    CreateEventSchema,
    UpdateEventSchema
)
from service.event import  (
    create_event_db,
    add_category_to_event_db,
    add_location_to_event_db,
    add_media_to_event_db,
    add_ticket_type_to_event_db,
    add_promotion_to_event_db,
    delete_event_db,
    update_event_db
)
from core.dependencies import (
    CustomerDependency,
    SessionDependency,
    OrganizerDependency
)
from service.like import create_like, delete_like

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.get("/", response_model=list[ResponseEventSchema])
async def get_all_event(db: SessionDependency):
    """Route to get all events.

    Args:
        db (SessionDependency): The database session

    Returns:
        list[EventSchema]: A list of all event objects
    """
    events = db.query(EventDB).all()
    return events

@router.get("/{id_event}", response_model=ResponseEventSchema)
async def get_event_by_id(id_event: int, db: SessionDependency) -> ResponseEventSchema:
    """Route to get an event by ID.

    Args:
        id_event (int): The ID of the event to retrieve
        db (SessionDependency): The database session

    Returns:
        EventSchema: The retrieved event object
    """
    event = db.query(EventDB).filter(EventDB.id_event == id_event).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/", response_model=ResponseEventSchema)
async def create_event(event: CreateEventSchema, current_user: OrganizerDependency, db: SessionDependency) -> ResponseEventSchema:
    new_event = create_event_db(
        id_organizer = current_user.id_user,
        name = event.name,
        start_date = event.start_date,
        end_date = event.end_date,
        creation_date= event.created_date,
        event_status = event.event_status,
        max_capacity = event.max_capacity,
        description = event.description,
        metadata = event.metadata,
        db = db
    )
    return new_event

@router.delete("/{event_id}")
async def delete_event(event_id: int, db: SessionDependency):
    delete_event_db(id_event= event_id, db= db)
    return Response(status_code=200, content="Delete success")

@router.put("/{event_id}")
async def update_event(event_id: int, new_event: UpdateEventSchema, organizer: OrganizerDependency, db:SessionDependency):
    update_event_db(new_event= new_event, event_id= event_id, db= db)
    return Response(status_code= 201, content= "Update success")

@router.post('/{event_id}/category/{category_id}')
async def add_category_to_event(event_id: int, category_id: int, db : SessionDependency) -> Response:
    add_category_to_event_db(event_id, category_id, db)
    return Response(status_code=200, content="category add")

@router.post('/{event_id}/location/{location_id}')
async def add_location_to_event(event_id: int, location_id: int, db: SessionDependency):
    add_location_to_event_db(event_id, location_id, db)
    return Response(status_code=200, content="location add")

@router.post('/{event_id}/media/{media_id}')
async def add_media_to_event(event_id: int, media_id: int, db: SessionDependency):
    add_media_to_event_db(event_id, media_id, db)
    return Response(status_code=200, content="media add")

@router.post('/{event_id}/ticket_type/{ticket_type_id}')
async def add_ticket_type_to_event(event_id: int, ticket_type_id: int, db: SessionDependency):
    add_ticket_type_to_event_db(event_id, ticket_type_id, db)
    return Response(status_code=200, content="ticket type add")

@router.post('/{event_id}/promotion/{promotion_id}')
async def add_promotion_to_event(event_id: int, promotion_id: int, db: SessionDependency):
    add_promotion_to_event_db(event_id, promotion_id, db)
    return Response(status_code=200, content="promotion add")

@router.post('/{event_id}/like')
async def like_event(event_id : int, customer: CustomerDependency, db : SessionDependency):
    create_like(id_customer= customer.id_user, id_event= event_id, db= db)
    return Response(status_code= 201, content= "Like cree avec succes")

@router.delete("/{event_id}/like")
async def unlike_event(event_id : int, customer: CustomerDependency, db : SessionDependency):
    delete_like(id_customer= customer.id_user, id_event= event_id, db= db)
    return Response(status_code= 200, content="Message supprimer avec succes")
