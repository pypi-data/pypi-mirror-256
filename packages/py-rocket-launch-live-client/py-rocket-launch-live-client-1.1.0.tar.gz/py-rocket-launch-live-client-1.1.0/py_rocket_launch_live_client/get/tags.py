import requests
import py_rocket_launch_live_client as prllc


def get(key: str, headers: dict = {}, id: int | None = None, text: str | None = None,
        limit: int | None = None, page_size: int = 25):
    params = {}
    prllc.auth.set_auth_header(key, headers)
    if id is not None:
        params['id'] = id
    if text is not None:
        params['text'] = text
    return prllc.cursor.RocketLaunchliveCursor('tags', headers=headers, params=params, limit=limit, page_size=page_size)
