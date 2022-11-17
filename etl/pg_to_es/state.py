from pydantic import BaseModel
from pendulum import DateTime


class EtlProcessingState(BaseModel):
    list_last_dt: list[int] = [{str: DateTime}]