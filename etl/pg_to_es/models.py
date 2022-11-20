from pathlib import Path
from uuid import UUID

from pendulum import Date
from pydantic import BaseModel, Field, validator


class UUIDMixin(BaseModel):
    id: UUID


class Person(UUIDMixin):
    name: str


class Movie(UUIDMixin):

    imdb_rating: float
    genre: list[str] | None
    title: str
    description: str | None
    director: str
    actors_names: list[str] | None
    writers_names: list[str] | None
    actors: list[Person]
    writers: list[Person]

    @validator('imdb_rating')
    def name_must_contain_space(cls, v):
        if v < 0:
            v = 0
        elif v > 100:
            v = 100
        return v


class ESIndex(BaseModel):
    id: UUID = Field(None, alias="_id")
    index: str = Field(None, alias="_index")


class ESIndexLine(BaseModel):
    index: ESIndex


class EtlState(BaseModel):
    date_from: Date | None
    date_to: Date | None
    step: int | None


class ExtractSettings(BaseModel):
    conn_params: dict
    schemas: str
    extract_path: Path
    sql_file: Path
    batches: int


class TransformSettings(BaseModel):
    transform_path: Path
    extract_path: Path
    index_name: str


class LoadSettings(BaseModel):
    conn_str: str
    index_name: str
    transform_path: Path
    schema_file_path: Path
