import os
import pytest
from functools import lru_cache
from octopusapi import ElectricityMeter
from datetime import datetime, timedelta
import pytz


@pytest.fixture
def api_key():
    return os.environ["OCTOPUS_API_KEY"]


@pytest.fixture
def electricity_mpan():
    return os.environ["OCTOPUS_ELECTRICITY_MPAN"]


@pytest.fixture
def electricity_serial_number():
    return os.environ["OCTOPUS_ELECTRICITY_SERIAL_NUMBER"]


@pytest.fixture
def grid_supply_points():
    return [
        "_A",
        "_B",
        "_C",
        "_D",
        "_E",
        "_F",
        "_G",
        "_H",
        "_J",
        "_K",
        "_L",
        "_M",
        "_N",
        "_P",
    ]


@pytest.fixture
def electricity_meter(api_key, electricity_mpan, electricity_serial_number):
    return ElectricityMeter(api_key, electricity_mpan, electricity_serial_number)


@pytest.fixture
@lru_cache
def test_end_time():
    test_start_time = datetime.now(tz=pytz.utc).replace(
        minute=0, second=0, microsecond=0
    )
    return test_start_time - timedelta(hours=24)
