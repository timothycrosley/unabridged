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
    async def create_(data: InModel):
        return await Model.from_tortoise_orm(await DBModel.create(**data.dict(exclude_unset=True)))


    @app.get(f"/{model_name}/{{id}}", response_model=Model, responses={404: {"model": HTTPNotFoundError}})
    async def get_(id: int):
        return await Model.from_queryset_single(DBModel.get(id=id))


    @app.put(f"/{model_name}/{{id}}", response_model=Model, responses={404: {"model": HTTPNotFoundError}})
    async def update_(id: int, data: InModel):
        await models.Model.filter(id=id).update(**data.dict(exclude_unset=True))
        return await Model.from_queryset_single(DBModel.get(id=id))


    @app.delete(
        f"/{model_name}/{{id}}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}
    )
    async def delete_(id: int):
        deleted_count = await DBModel.filter(id=id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"{model_name.capitalize()} {id} not found")
        return Status(message=f"Deleted {model_name} {id}")


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["unabridged.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
