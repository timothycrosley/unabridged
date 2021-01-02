from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Event, State

Event = pydantic_model_creator(Event)
State = pydantic_model_creator(State)
