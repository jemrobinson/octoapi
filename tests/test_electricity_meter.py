from datetime import datetime, timedelta
import pytest
from octopusapi import ElectricityMeter, ApiException


def test_electricity_meter_non_existence(api_key):
    electricity_meter = ElectricityMeter(api_key, "fake-mpan", "fake-serial-number")
    with pytest.raises(ApiException):
        electricity_meter.verify()


def test_electricity_meter_existence(
    electricity_meter, electricity_mpan, grid_supply_points
):
    meter_details = electricity_meter.verify()
    assert meter_details["mpan"] == electricity_mpan
    assert meter_details["gsp"] in grid_supply_points
    assert isinstance(meter_details["profile_class"], int)


def test_electricity_meter_consumption(electricity_meter):
    consumption = electricity_meter.consumption()
    assert isinstance(consumption[0]["consumption"], float)
    assert isinstance(consumption[0]["interval_start"], datetime)
    assert isinstance(consumption[0]["interval_end"], datetime)


def test_electricity_meter_consumption_halfhourly(electricity_meter, test_end_time):
    start_time = test_end_time - timedelta(hours=24)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time
    )
    assert len(consumption) == 47


def test_electricity_meter_consumption_hourly(electricity_meter, test_end_time):
    start_time = test_end_time - timedelta(hours=24)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time, group_by="hour"
    )
    assert len(consumption) == 23


def test_electricity_meter_consumption_daily(electricity_meter, test_end_time):
    start_time = test_end_time - timedelta(days=1)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time, group_by="day"
    )
    assert len(consumption) == 1


def test_electricity_meter_consumption_weekly(electricity_meter, test_end_time):
    start_time = test_end_time - timedelta(days=14)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time, group_by="week"
    )
    assert len(consumption) == 2


def test_electricity_meter_consumption_monthly(electricity_meter, test_end_time):
    start_time = test_end_time - timedelta(days=31)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time, group_by="month"
    )
    assert len(consumption) in [0, 1, 2]


def test_electricity_meter_consumption_quarterly(electricity_meter, test_end_time):
    start_time = test_end_time - timedelta(days=31)
    consumption = electricity_meter.consumption(
        period_from=start_time, period_to=test_end_time, group_by="quarter"
    )
    assert len(consumption) in [0, 1]
