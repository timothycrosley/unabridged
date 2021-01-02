from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_models import Event
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

app = FastAPI(title="Unabridged activity API")


class Status(BaseModel):
    message: str


@app.get("/events", response_model=List[Event])
async def get_events():
    return await Event.from_queryset(Event.all())


@app.post("/events", response_model=Event)
async def create_event(event: Event):
    event_obj = await Event.create(**event.dict(exclude_unset=True))
    return await Event.from_tortoise_orm(event_obj)


@app.get("/event/{event_id}", response_model=Event, responses={404: {"model": HTTPNotFoundError}})
async def get_event(event_id: int):
    return await Event.from_queryset_single(Event.get(id=event_id))


@app.put("/event/{user_id}", response_model=Event, responses={404: {"model": HTTPNotFoundError}})
async def update_event(event_id: int, event: Event):
    await Event.filter(id=event_id).update(**event.dict(exclude_unset=True))
    return await Event.from_queryset_single(Event.get(id=event_id))


@app.delete(
    "/event/{event_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}
)
async def delete_event(event_id: int):
    deleted_count = await Event.filter(id=event_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
    return Status(message=f"Deleted event {event_id}")


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
