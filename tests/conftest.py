from datetime import datetime, timedelta
from functools import lru_cache
import os
from pathlib import Path
import pytest
import pytz
import toml
from octoapi import ElectricityMeter

# pylint: disable=unused-argument,redefined-outer-name

def config():
    """Attempt to load config file"""
    config_path = Path(__file__).resolve().parents[1].joinpath("user_config.toml")
    try:
        with open(config_path, "r") as f_config:
            config = toml.loads(f_config.read())
        return config
    except (FileNotFoundError, toml.decoder.TomlDecodeError):
        return {}


@pytest.fixture
def api_key(scope="module"):
    """Get API key from config or environment variable"""
    try:
        api_key = config()["general"]["api_key"]
    except KeyError:
        api_key = os.environ["OCTOPUS_API_KEY"]
    return api_key


@pytest.fixture
def electricity_mpan(scope="module"):
    """Get electricity meter MPAN from config or environment variable"""
    try:
        mpan = config()["electricity"]["mpan"]
    except KeyError:
        mpan = os.environ["OCTOPUS_ELECTRICITY_MPAN"]
    return mpan


@pytest.fixture
def electricity_serial_number(scope="module"):
    """Get electricity meter serial number from config or environment variable"""
    try:
        serial = config()["electricity"]["serial_number"]
    except KeyError:
        serial = os.environ["OCTOPUS_ELECTRICITY_SERIAL_NUMBER"]
    return serial


@pytest.fixture
def grid_supply_points(scope="module"):
    """Get allowable grid supply points"""
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
def electricity_meter(
    api_key: str,
    electricity_mpan: str,
    electricity_serial_number: str,
    scope: str = "module",
) -> ElectricityMeter:
    """Get an ElectricityMeter fixture

    :Keyword Arguments:
        * **api_key**: (*str) -- API key.
        * **electricity_mpan**: (*str) -- electricity meter MPAN.
        * **electricity_serial_number**: (*str*) -- electricity meter serial number.
    """
    return ElectricityMeter(api_key, electricity_mpan, electricity_serial_number)


@pytest.fixture
@lru_cache(maxsize=1)
def test_end_time(scope="module"):
    """Get the end time used in subsequent tests.
    We use 24hours ago, rounded down to the nearest hour
    """
    test_start_time = datetime.now(tz=pytz.utc).replace(
        minute=0, second=0, microsecond=0
    )
    return test_start_time - timedelta(days=7)
