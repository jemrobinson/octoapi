from typing import Any, Optional
from datetime import datetime
from dateutil import parser
from .types import JSONType
from .exceptions import ParameterException


class MeterMixin:
    def __init__(
        self, meter_id: str, serial_number: str, meter_type: str, **kwargs: Any
    ) -> None:
        self.meter_id = meter_id
        self.serial_number = serial_number
        self.meter_type = meter_type

        # Pass unused arguments onwards
        super().__init__(**kwargs)

    def consumption(
        self,
        period_from: Optional[datetime] = None,
        period_to: Optional[datetime] = None,
        page_size: Optional[int] = None,
        reverse: Optional[bool] = False,
        group_by: Optional[str] = None,
    ) -> JSONType:
        # Validate parameters
        params = {}
        if period_from:
            params["period_from"] = period_from.isoformat()
        if period_to:
            params["period_to"] = period_to.isoformat()
        if page_size:
            params["page_size"] = page_size
        if reverse:
            params["order_by"] = "period"
        if group_by:
            allowed_groupings = ["hour", "day", "week", "month", "quarter"]
            if not group_by in allowed_groupings:
                raise ParameterException(
                    "'group_by' must be one of %s", allowed_groupings
                )
            params["group_by"] = group_by
        # Retrieve JSON
        json_response = self.request_json(
            path=f"{self.meter_type}/{self.meter_id}/meters/{self.serial_number}/consumption/",
            params=params,
        )
        # Format output
        results = [
            {
                "consumption": float(entry["consumption"]),
                "interval_start": parser.parse(entry["interval_start"]),
                "interval_end": parser.parse(entry["interval_end"]),
            }
            for entry in json_response["results"]
        ]
        # Enforce exclusive period_to
        if period_to:
            return [r for r in results if r["interval_end"] < period_to]
        return results

    def verify(self) -> JSONType:
        return self.request_json(path=f"{self.meter_type}/{self.meter_id}/")
