from enum import IntEnum

from tortoise import fields
from tortoise.models import Model

Reaction = IntEnum("Reaction", "NONE HATED DISLIKED INDIFFERENT LIKED LOVED")


class Event(Model):
    id = fields.IntField(pk=True)
    kind = fields.CharField(200)
    name = fields.CharField(200)
    description = fields.TextField(default="")
    comments = fields.TextField(default="")
    reaction: Reaction = fields.IntEnumField(Reaction, default=Reaction.NONE)
    created = fields.DatetimeField(auto_now_add=True)


class State(Event):
    completed = fields.DatetimeField()
