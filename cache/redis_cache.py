import json
from redis import Redis, DataError, ConnectionError
from utils.utils import datetime_serializer, datetime_deserializer


class RedisCache:
    def __init__(self, config: dict):
        self.config = config
        self.conn = self._connect()

    def _connect(self):
        conn = Redis(**self.config)
        return conn

    def set_value(self, name: str, value_dict: dict, ttl: int):
        value_js = json.dumps(value_dict, default=datetime_serializer)
        try:
            self.conn.set(name=name, value=value_js)
            if ttl > 0:
                self.conn.expire(name, ttl)
                return True
        except DataError as err:
            print(err)
            return False

    def get_value(self, name: str):
        value_js = self.conn.get(name)
        if value_js:
            value_dict = json.loads(value_js, object_hook=datetime_deserializer)
            return value_dict
        else:
            return None
