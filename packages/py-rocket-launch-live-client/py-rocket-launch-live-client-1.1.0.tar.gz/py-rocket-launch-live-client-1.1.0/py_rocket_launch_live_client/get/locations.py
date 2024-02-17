
import requests
import py_rocket_launch_live_client as prllc


def get(key: str, headers: dict = {}, id: int | None = None, name: str | None = None, state: str | None = None, country: str = 'US',
        limit: int | None = None, page_size: int = 25):
    params = {}
    prllc.auth.set_auth_header(key, headers)
    if id is not None:
        params['id'] = id
    if name is not None:
        params['name'] = name
    if state is not None:
        params['state_abbr'] = state
    if country is not None:
        params['country_code'] = country
    return prllc.cursor.RocketLaunchliveCursor('locations', headers=headers, params=params, limit=limit,page_size=page_size)
