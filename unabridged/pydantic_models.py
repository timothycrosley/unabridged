from tortoise.contrib.pydantic import pydantic_model_creator

from . import models

Event = pydantic_model_creator(models.Event)
State = pydantic_model_creator(models.State)
