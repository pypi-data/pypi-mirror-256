

def set_auth_header(token: str, headers: dict = {}):
    headers['Authorization'] = f'Bearer {token}'


def set_auth_param(token: str, params: dict = {}):
    params['key'] = token
