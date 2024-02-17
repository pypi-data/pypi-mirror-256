import py_rocket_launch_live_client as prllc


def test_state_code_const():
    assert prllc.us_states.AZ == 'AZ'
    