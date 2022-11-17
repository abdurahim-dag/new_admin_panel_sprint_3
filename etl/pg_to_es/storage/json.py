from base import BaseStorage
import json
from typing import Optional
import pathlib


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path
        self.path = pathlib.Path(self.file_path)

    def save_state(self, state:dict):
        with open(self.file_path, 'w') as f:
            json.dump(state, f)

    def retrieve_state(self) -> dict:
        result = {}
        if self.path.exists() and self.path.is_file():
            with open(self.path, 'r') as f:
                result = json.load(f)
        return result
