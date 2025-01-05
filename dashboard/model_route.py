from dataclasses import dataclass
from database.select import select_list, select_dict
from database.procedure import call_proc, call_proc_state
from cache.wrapper import fetch_from_cache
from datetime import date


@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool


def getbills(db_config, sql_provider, cache_config, user_login):
    cache_select_dict = fetch_from_cache('client_bills', cache_config)(select_dict)
    _sql = sql_provider.get('get_bills.sql', user_login=user_login)
    result = cache_select_dict(db_config, _sql)
    if result:
        return ProductInfoRespronse(result, error_message="", status=True)
    return ProductInfoRespronse(result, error_message="Ошибка сервера", status=False)


def newbill(db_config, sql_provider, user_data):
    _sql = sql_provider.get('user_verification.sql', user_login=user_data['login'])
    result1, schema = select_list(db_config, _sql)
    if not schema:
        return ProductInfoRespronse((), error_message="Ошибка сервера", status=False)
    if not result1:
        return ProductInfoRespronse((), error_message="Пользователь не существует", status=False)
    res = None
    result = call_proc(db_config, 'create_bill', (user_data['login'], user_data['currency'], res))
    if result:
        return ProductInfoRespronse(result[2], error_message="", status=True)
    return ProductInfoRespronse(result, error_message="Произошла ошибка при создании нового счёта", status=False)


def gethistory(db_config, sql_provider, user_login, detail: str=" "):
    _sql = sql_provider.get('get_bill_history.sql',
                            user_login=user_login,
                            detail=detail)
    result, schema = select_list(db_config, _sql)
    if result or schema:
        return ProductInfoRespronse(result, error_message="", status=True)
    return ProductInfoRespronse(result, error_message="Ошибка при получении истории внешних операций.", status=False)


def getinnerhistory(db_config, sql_provider, user_login, detail : str=" "):
    _sql = sql_provider.get('get_bill_history_inner.sql',
                            user_login=user_login,
                            detail=detail)
    result, schema = select_list(db_config, _sql)
    if result or schema:
        return ProductInfoRespronse(result, error_message="", status=True)
    return ProductInfoRespronse(result, error_message="Ошибка при получении истории внтренних операций.", status=False)


def gethistorydetails(db_config, sql_provider, bill_id, change_date):
    _sql = sql_provider.get('get_bill_history_details.sql',
                            change_date=change_date,
                            bill_id=bill_id)
    result, schema = select_list(db_config, _sql)
    if result:
        return ProductInfoRespronse(result, error_message="", status=True)
    return ProductInfoRespronse(result,
                                error_message="Ошибка при получении информации о переводе.",
                                status=False)


def getcurrencies(db_config, sql_provider):
    _sql = sql_provider.get('get_currency.sql')
    result, schema = select_list(db_config, _sql)
    if result:
        return ProductInfoRespronse(result, error_message="", status=True)
    return ProductInfoRespronse(result, error_message="Ошибка при получении доступных валют.", status=False)


def transfer(db_config, sql_provider, user_data):
    result = call_proc_state(db_config, 'transfer', (user_data['sender_bill'],
                                                     user_data['receiver_bill'], user_data['amount']))
    if not result:
        return ProductInfoRespronse((), error_message="", status=True)
    return ProductInfoRespronse((result.args[0], result.args[1]), error_message=result.args[1], status=False)


def findbill(db_config, sql_provider, user_data):
    _sql = sql_provider.get('find_bill.sql', receiver_login=user_data[0], sender_bill=user_data[1])
    result, schema = select_list(db_config, _sql)
    if not schema:
        return ProductInfoRespronse((), error_message="Ошибка сервера.", status=False)
    if not result:
        return ProductInfoRespronse((), error_message="Cчёт с соответствующей валютой не был найден у получателя.",
                                    status=False)
    return ProductInfoRespronse(result[0][0], error_message="", status=True)


def getuserinfo(db_config, sql_provider, user_login):
    _sql = sql_provider.get('get_user_info.sql', user_login=user_login)
    result, schema = select_list(db_config, _sql)
    if not schema:
        return ProductInfoRespronse((), error_message="Ошибка сервера.", status=False)
    if not result:
        return ProductInfoRespronse((), error_message="Ошибка при получении данных пользователя.",
                                    status=False)
    result = list(result[0])
    result[2] = (result[2]).strftime("%d.%m.%Y")
    result[5] = (result[5]).strftime("%d.%m.%Y")

    return ProductInfoRespronse(result, error_message="", status=True)


def getworkerinfo(db_config, sql_provider, user_login):
    _sql = sql_provider.get('get_worker_info.sql', user_login=user_login)
    result, schema = select_list(db_config, _sql)
    if not schema:
        return ProductInfoRespronse((), error_message="Ошибка сервера.", status=False)
    if not result:
        return ProductInfoRespronse((), error_message="Ошибка при получении данных пользователя.",
                                    status=False)
    return ProductInfoRespronse(result[0], error_message="", status=True)


def getbilldetalisation(db_config, sql_provider, user_login, begin_date, end_date):
    _sql = sql_provider.get('get_bills.sql', user_login=user_login)
    result, schema = select_list(db_config, _sql)
    if not schema:
        return ProductInfoRespronse((), error_message="Ошибка сервера.", status=False)
    if not result:
        return ProductInfoRespronse((), error_message="", status=True)

    bills = [(i[0],i[1]) for i in result] # номер счёта и валюта
    print(bills)
    bill_detalisation = []
    # item in bill_detalisation: bill_id, currency, total_deposit, total_withdraw, total_transfer_out, total_transfer_in

    for item in bills:
        _sql = sql_provider.get('detalisation_bill_history.sql',
                                bill_id=item[0],
                                begin_date=begin_date,
                                end_date=end_date)
        result, schema = select_list(db_config, _sql)

        if not schema:
            return ProductInfoRespronse((), error_message="Ошибка сервера.", status=False)
        if result:
            result = result[0]
            bill_detalisation.append([item[0], item[1], result[0], result[1], result[2], result[3]])
    return ProductInfoRespronse(tuple(bill_detalisation), error_message="", status=True)


def getbilldetalisationinner(db_config, sql_provider, user_login, begin_date, end_date):
    _sql = sql_provider.get('get_bills.sql', user_login=user_login)
    result, schema = select_list(db_config, _sql)
    if not schema:
        return ProductInfoRespronse((), error_message="Ошибка сервера.", status=False)
    if not result:
        return ProductInfoRespronse((), error_message="", status=True)

    bills = [(i[0], i[1]) for i in result]  # номер счёта и валюта
    bill_detalisation = []
    # item in bill_detalisation: bill_id, currency, total_withdrawal, total_deposit
    for item in bills:
        _sql = sql_provider.get('detalisation_bill_history_inner.sql',
                                bill_id=item[0],
                                begin_date=begin_date,
                                end_date=end_date)
        result, schema = select_list(db_config, _sql)
        if not schema:
            return ProductInfoRespronse((), error_message="Ошибка сервера.", status=False)
        if result:
            result = result[0]
            if not (result[0] == result[1] == 0):
                bill_detalisation.append([item[0], item[1], result[0], result[1]])
    return ProductInfoRespronse(tuple(bill_detalisation), error_message="", status=True)


def deposit_manager(db_config, sql_provider, user_data, login):
    _sql = sql_provider.get('worker_verification.sql', worker_login=login)
    result, schema = select_list(db_config, _sql)
    if not schema:
        return ProductInfoRespronse((), error_message="Ошибка сервера.", status=False)
    if not result:
        return ProductInfoRespronse((), error_message="Идентификационный номер не был найден.", status=False)
    result = call_proc_state(db_config, 'deposit', (user_data.get('amount'), user_data.get('account_number'), result[0][0]))
    if not result:
        return ProductInfoRespronse((), error_message="", status=True)
    return ProductInfoRespronse((result.args[0], result.args[1]), error_message=result.args[1], status=False)


def withdraw_manager(db_config, sql_provider, user_data, login):
    _sql = sql_provider.get('worker_verification.sql', worker_login=login)
    result, schema = select_list(db_config, _sql)
    if not schema:
        return ProductInfoRespronse((), error_message="Ошибка сервера.", status=False)
    if not result:
        return ProductInfoRespronse((), error_message="Идентификационный номер не был найден.", status=False)
    result = call_proc_state(db_config, 'withdraw', (user_data.get('amount'), user_data.get('account_number'), result[0][0]))
    if not result:
        return ProductInfoRespronse((), error_message="", status=True)
    return ProductInfoRespronse((result.args[0], result.args[1]), error_message=result.args[1], status=False)









