from fastapi import FastAPI
from routes import (
    events,
    customer,
    organizer,
    category,
    auth,
    bookings,
    waiting_list,
    ticket_type_event,
    location,
    media,
    promotion,
    user,
    like
)

app = FastAPI(
    title="API AtlaxOasis 2026",
    version="0.1.0",
    root_path="/api"
)

app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(category.router)
app.include_router(customer.router)
app.include_router(events.router)
app.include_router(location.router)
app.include_router(media.router)
app.include_router(organizer.router)
app.include_router(promotion.router)
app.include_router(ticket_type_event.router)
app.include_router(user.router)
app.include_router(waiting_list.router)
app.include_router(like.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)