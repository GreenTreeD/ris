from dataclasses import dataclass
from database.insert import insert_one
from database.select import select_string
from datetime import date


@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool


def auth(db_config, user_input_data, sql_provider):
    error_message = ''
    _sql = sql_provider.get('users.sql', login=user_input_data['login'], password=user_input_data['password'])
    result, schema = select_string(db_config, _sql)
    if not schema:
        return ProductInfoRespronse(result, error_message=error_message, status=False)
    if result:
        result = list(result[0])
        result.append('user')
        return ProductInfoRespronse(tuple(result), error_message="", status=True)
    _sql = sql_provider.get('workers.sql', login=user_input_data['login'], password=user_input_data['password'])
    result, schema = select_string(db_config, _sql)
    if not schema:
        return ProductInfoRespronse(result, error_message=error_message, status=False)
    if result or schema:
        if result:
            return ProductInfoRespronse(result[0], error_message="", status=True)
        return ProductInfoRespronse(result, error_message="", status=True)


def exist_check(db_config, user_input_data, sql_provider):
    if user_input_data.get('user_role'):
        _sql = sql_provider.get('check_exist.sql', user_login=user_input_data['login'], table='workers')
    else:
        _sql = sql_provider.get('check_exist.sql', user_login=user_input_data['login'], table='user')
    print(_sql)
    result, schema = select_string(db_config, _sql)
    if not schema:
        return ProductInfoRespronse(result, error_message="Ошибка сервера", status=False)
    if result:
        return ProductInfoRespronse(result, error_message="Такой пользователь уже существует", status=False)
    return ProductInfoRespronse((), error_message="", status=True)


def reg_new(db_config, user_input_data, sql_provider):
    error_message = "Ошибка сервера"
    if user_input_data.get('user_role'):
        _sql = sql_provider.get('workers_new.sql',
                                user_role=user_input_data['user_role'],
                                surname=user_input_data['surname'],
                                login=user_input_data['login'],
                                password=user_input_data['password'])
    else:
        _sql = sql_provider.get('users_new.sql',
                                surname=user_input_data['surname'],
                                bday=user_input_data['bday'],
                                address=user_input_data['address'],
                                phone_num=user_input_data['tel'],
                                login=user_input_data['login'],
                                contract_date=date.today().isoformat(),
                                password=user_input_data['password'])
    result = insert_one(db_config, _sql)
    if result:
        return ProductInfoRespronse(tuple(), error_message="", status=True)
    return ProductInfoRespronse(tuple(), error_message=error_message, status=False)
