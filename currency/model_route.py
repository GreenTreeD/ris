from dataclasses import dataclass
from database.select import select_list
from database.insert import insert_one
from datetime import date


@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool


def get_currency_names(db_config, sql_provider):
    error_message = ''
    _sql = sql_provider.get('currency_names.sql')
    result, schema = select_list(db_config, _sql)
    if result or schema:
        if result:
            res = [i[0] for i in result]
            res = tuple(res)
            return ProductInfoRespronse(res, error_message=error_message, status=True)
        return ProductInfoRespronse(result, error_message=error_message, status=True)
    return ProductInfoRespronse(result, error_message="Ошибка сервера", status=False)


def get_currency_rate(db_config, sql_provider, to_currency):
    _sql = sql_provider.get('get_currency.sql', today=date.today(), to_currency=to_currency)
    result, schema = select_list(db_config, _sql)
    if result or schema:
        return ProductInfoRespronse(result, error_message="", status=True)
    return ProductInfoRespronse(result, error_message="Ошибка сервера", status=False)


def set_currency_rates(db_config, sql_provider, info):
    currency_dict = dict()
    _sql = sql_provider.get('currency_names_set.sql')
    result, schema = select_list(db_config, _sql)
    if not (result or schema):
        return ProductInfoRespronse(result, error_message="Ошибка сервера. Изменения не были сохранены.", status=False)
    for i in result:
        currency_dict[i[1]] = i[0]

    string = ""
    for k, v in info.items():
        cur = k.split("_")
        string+=f"({currency_dict[cur[0]]}, {currency_dict[cur[1]]}, {v}, '{date.today()}'),"
    string = string[:-1]
    string+=";"

    _sql = sql_provider.get('set_currency.sql', info=string)
    print(_sql)
    result = insert_one(db_config, _sql)
    if result:
        return ProductInfoRespronse(result, error_message="", status=True)
    return ProductInfoRespronse(result, error_message="Ошибка сервера. Изменения не были сохранены.", status=False)





