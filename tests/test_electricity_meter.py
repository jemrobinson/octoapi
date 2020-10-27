from octopusapi import __version__
from octopusapi import ElectricityMeter
from .fixtures import *
import pytest


@pytest.fixture
def electricity_meter(api_key, electricity_mpan, electricity_serial_number):
    return ElectricityMeter(api_key, electricity_mpan, electricity_serial_number)


def test_version():
    assert __version__ == "0.1.0"


def test_have_api_key(api_key):
    assert api_key is not None


def test_electricity_meter_existence(
    electricity_meter, electricity_mpan, grid_supply_points
):
    meter_details = electricity_meter.verify()
    assert meter_details["mpan"] == electricity_mpan
    assert meter_details["gsp"] in grid_supply_points
    assert isinstance(meter_details["profile_class"], int)
