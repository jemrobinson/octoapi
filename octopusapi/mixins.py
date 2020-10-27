from typing import Any
from .types import JSONType


class MeterMixin:
    def __init__(
        self, meter_id: str, serial_number: str, meter_type: str, **kwargs: Any
    ) -> None:
        self.meter_id = meter_id
        self.serial_number = serial_number
        self.meter_type = meter_type

        # Pass unused arguments onwards
        super().__init__(**kwargs)

    def consumption(self) -> JSONType:
        return self.request_json(
            path=f"{self.meter_type}/{self.meter_id}/meters/{self.serial_number}/consumption/"
        )

    def verify(self) -> JSONType:
        return self.request_json(path=f"{self.meter_type}/{self.meter_id}/")
