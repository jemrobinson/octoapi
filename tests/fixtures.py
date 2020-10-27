import os
import pytest


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
