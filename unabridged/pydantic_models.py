from tortoise.contrib.pydantic import pydantic_model_creator

from . import models


class Event(pydantic_model_creator(models.Event)):  # type: ignore
    pass


class EventIn(
    pydantic_model_creator(models.Event, name="Event", exclude_readonly=True)  # type: ignore
):
    pass


class State(pydantic_model_creator(models.State)):  # type: ignore
    pass


class StateIn(
    pydantic_model_creator(models.State, name="State", exclude_readonly=True)  # type: ignore
):
    pass
