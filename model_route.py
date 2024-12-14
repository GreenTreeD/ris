from base64 import b64encode
from dataclasses import dataclass
from database.select import select_list

@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool


def create_basic_auth_token(login, password):
    credentials = b64encode(f'{login}:{password}'.encode('ascii')).decode('ascii')
    token = f'Basic {credentials}'
    return token

