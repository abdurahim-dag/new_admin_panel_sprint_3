from pendulum import datetime
from pydantic import BaseModel
from uuid import UUID
from pydantic import BaseModel, ValidationError, validator


class TimeStampedMixin(BaseModel):
    created: datetime
    modified: datetime


class UUIDMixin(BaseModel):
    id: UUID


class Person(UUIDMixin):
    name: str


class Actor(Person):
    pass


class Writer(UUIDMixin):
    pass


class Movies(UUIDMixin, TimeStampedMixin):

    imdb_rating: int
    genre: list[str] | None
    title: str
    description: str | None
    director: str
    actors_names: list[str] | None
    actors: list[Actor]
    writers: list[Writer]

    @validator('imdb_rating')
    def raiting_must_range(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Must be in rage: [0,100]')
