
import requests
import py_rocket_launch_live_client as prllc

def get(key: str, headers: dict = {}, 
        id: int | None = None, 
        cospar_id:str | None = None,
        after_date:str | None = None,
        before_date:str | None = None,
        modified_since:str | None = None,
        location_id:int | None = None,
        pad_id:int | None = None,
        provider_id:int | None = None,
        tag_id:int | None = None,
        vehicle_id:int | None = None,
        state_abbr:str | None = None,
        country_code:str | None = None,
        search:str | None = None,
        slug:str | None = None,
        limit:int | None = None,
        direction:prllc.codes.Direction | None = None,
        page_size:int = 25
        ):
    params = {}
    if id is not None:
        params['id'] = id
    if cospar_id is not None:
        params['cospar_id'] = cospar_id
    if after_date is not None:
        params['after_date'] = after_date
    if before_date is not None:
        params['before_date'] = before_date
    if modified_since is not None:
        params['modified_since'] = modified_since
    if location_id is not None:
         params['location_id'] = location_id
    if pad_id is not None:
        params['pad_id'] = pad_id
    if provider_id is not None:
        params['provider_id'] = provider_id
    if tag_id is not None:
        params['tag_id'] = tag_id
    if vehicle_id is not None:
        params['vehicle_id'] = vehicle_id
    if state_abbr is not None:
        params['state_abbr'] = state_abbr
    if country_code is not None:
        params['country_code'] = country_code
    if search is not None:
        params['search'] = search
    if slug is not None:
        params['slug'] = slug
    if direction is not None:
        params['direction'] = direction 
    prllc.auth.set_auth_header(key, headers)
    return prllc.cursor.RocketLaunchliveCursor('launches', headers=headers, params=params,limit=limit,page_size=page_size)
