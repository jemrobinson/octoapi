def test_have_api_key(api_key):
    """Test the api_key fixture"""
    assert api_key is not None


def test_have_electricity_mpan(electricity_mpan):
    """Test the electricity_mpan fixture"""
    assert electricity_mpan is not None


def test_have_electricity_serial_number(electricity_serial_number):
    """Test the electricity_serial_number fixture"""
    assert electricity_serial_number is not None
