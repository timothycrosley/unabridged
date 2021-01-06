from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from .pydantic_models import Event, EventIn, State, StateIn
from . import models

app = FastAPI(title="Unabridged activity API")


class Status(BaseModel):
    message: str

for model_name, Model, InModel, DBModel in (
    ('event', Event, EventIn, models.Event),
    ('state', State, StateIn, models.State),
):
    @app.get(f"/{model_name}s", response_model=List[Model])
    async def get_all_():
        return await Model.from_queryset(DBModel.all())


    @app.post(f"/{model_name}s", response_model=Model)
    async def create_(event: InModel):
        event_obj = await DBModel.create(**event.dict(exclude_unset=True))
        return await Model.from_tortoise_orm(event_obj)


    @app.get(f"/{model_name}/{{event_id}}", response_model=Model, responses={404: {"model": HTTPNotFoundError}})
    async def get_(event_id: int):
        return await Model.from_queryset_single(DBModel.get(id=event_id))


    @app.put(f"/{model_name}/{{user_id}}", response_model=Model, responses={404: {"model": HTTPNotFoundError}})
    async def update_(event_id: int, event: InModel):
        await models.Model.filter(id=event_id).update(**event.dict(exclude_unset=True))
        return await Model.from_queryset_single(DBModel.get(id=event_id))


    @app.delete(
        f"/{model_name}/{{event_id}}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}
    )
    async def delete_(event_id: int):
        deleted_count = await DBModel.filter(id=event_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
        return Status(message=f"Deleted event {event_id}")


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["unabridged.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
