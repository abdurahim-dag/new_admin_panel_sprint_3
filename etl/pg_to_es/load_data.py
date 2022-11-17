from storage.base import BaseStorage
from pathlib import Path
from state import EtlProcessingState

class EtlProcessing():

    file_status = '.RUNING'

    def _set_run_status(self):
        open(self.file_status, 'w')

    def _check_run_status(self):
        path = Path(self.file_status)
        if path.exists():
            raise Exception('Параллельно работает такой же процесс!')

    def __init__(
            self,
            storage: BaseStorage
    ):
        self.storage = storage
        external_data = self.storage.retrieve_state()
        self.state = EtlProcessingState(**external_data)

        self._check_run_status()
        self._set_run_status()

