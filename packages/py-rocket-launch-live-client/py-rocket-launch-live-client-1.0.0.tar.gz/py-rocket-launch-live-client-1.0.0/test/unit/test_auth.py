import py_rocket_launch_live_client as prllc


def test_set_auth_header():
    headers = {}
    prllc.auth.set_auth_header('1234',headers)
    assert 'Authorization' in headers,'authorization header not found'
    assert headers['Authorization'] == 'Bearer 1234'

def test_set_auth_param():
    params = {}
    prllc.auth.set_auth_param('1234',params)
    assert 'key' in params,'authorization key not found'
    assert params['key'] == '1234'
