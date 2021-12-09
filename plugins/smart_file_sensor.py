from airflow.sensors.filesystem import FileSensor
from typing import Any

class SmartFileSensor(FileSensor):
    poke_context_fields = ('filepath', 'fs_conn_id') # <- Required

    def __init__(self,  **kwargs: Any):
        super().__init__(**kwargs)

    def is_smart_sensor_compatible(self): # <- Required
        result = (
            not self.soft_fail
            and super().is_smart_sensor_compatible()
        )
        return result