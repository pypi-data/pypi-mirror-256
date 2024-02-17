import py_rocket_launch_live_client as prllc


def test_country_code_const():
    assert prllc.countries.CA == 'CA'
    assert prllc.countries.US == 'US'