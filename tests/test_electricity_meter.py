from datetime import datetime, timedelta
import pytest
from octopusapi import ElectricityMeter, ApiException


def test_electricity_meter_non_existence(api_key: str) -> None:
    """Test that a non-existent electricity meter throws an exception"""
    electricity_meter = ElectricityMeter(api_key, "fake-mpan", "fake-serial-number")
    with pytest.raises(ApiException):
        electricity_meter.verify()


def test_electricity_meter_existence(
    electricity_meter: ElectricityMeter, electricity_mpan: str, grid_supply_points: str
) -> None:
    """Test that the electricity meter end point has the right structure"""
    meter_details = electricity_meter.verify()
    assert meter_details["mpan"] == electricity_mpan
    assert meter_details["gsp"] in grid_supply_points
    assert isinstance(meter_details["profile_class"], int)


def test_electricity_meter_consumption(electricity_meter: ElectricityMeter) -> None:
    """Test that the electricity meter consumption end point has the right structure"""
    consumption = electricity_meter.consumption()
    assert isinstance(consumption[0]["consumption"], float)
    assert isinstance(consumption[0]["interval_start"], datetime)
    assert isinstance(consumption[0]["interval_end"], datetime)


def test_electricity_meter_consumption_halfhourly(
    electricity_meter: ElectricityMeter, test_end_time: datetime
) -> None:
    """Test that the electricity meter consumption end point works with half-hourly data"""
    start_time = test_end_time - timedelta(hours=24)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time
    )
    assert len(consumption) <= 47


def test_electricity_meter_consumption_hourly(
    electricity_meter: ElectricityMeter, test_end_time: datetime
) -> None:
    """Test that the electricity meter consumption end point works with hourly data"""
    start_time = test_end_time - timedelta(hours=24)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time, group_by="hour"
    )
    assert len(consumption) <= 23


def test_electricity_meter_consumption_daily(
    electricity_meter: ElectricityMeter, test_end_time: datetime
) -> None:
    """Test that the electricity meter consumption end point works with daily data"""
    start_time = test_end_time - timedelta(days=1)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time, group_by="day"
    )
    assert len(consumption) <= 1


def test_electricity_meter_consumption_weekly(
    electricity_meter: ElectricityMeter, test_end_time: datetime
) -> None:
    """Test that the electricity meter consumption end point works with weekly data"""
    start_time = test_end_time - timedelta(days=14)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time, group_by="week"
    )
    assert len(consumption) <= 2


def test_electricity_meter_consumption_monthly(
    electricity_meter: ElectricityMeter, test_end_time: datetime
) -> None:
    """Test that the electricity meter consumption end point works with monthly data"""
    start_time = test_end_time - timedelta(days=31)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time, group_by="month"
    )
    assert len(consumption) <= 2


def test_electricity_meter_consumption_quarterly(
    electricity_meter: ElectricityMeter, test_end_time: datetime
) -> None:
    """Test that the electricity meter consumption end point works with quarterly data"""
    start_time = test_end_time - timedelta(days=90)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time, group_by="quarter"
    )
    assert len(consumption) <= 1
