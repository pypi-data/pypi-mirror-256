
import requests
import py_rocket_launch_live_client as prllc


def get(key: str, headers: dict = {}, id: int | None = None, name: str | None = None, country: str = 'US', inactive: prllc.codes.Truth | None = None, 
        limit: int | None = None, page_size:int = 25):
    params = {}
    prllc.auth.set_auth_header(key, headers)
    if id is not None:
        params['id'] = id
    if name is not None:
        params['name'] = name
    if country is not None:
        params['country_code'] = country
    if inactive is not None:
        params['inactive'] = inactive.value
    return prllc.cursor.RocketLaunchliveCursor('companies', headers=headers, params=params,limit=limit,page_size=page_size)
