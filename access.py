from functools import wraps
from flask import session, request
import json
from utils.utils import render_with_defaults


def login_required(func):
    @wraps(func)
    def wrapper(*argc, **kwargs):
        if 'user_login' in session:
            return func(*argc, **kwargs)
        else:
            return render_with_defaults("error.html", message="Вы не авторизированы.Авторизируйтесь для продолжения работы.")
    return wrapper


def role_required(role: list):
    def wrap_out(func):
        @wraps(func)
        def wrap_in(*args, **kwargs):
            if 'user_role' in session:
                user_role = session.get('user_role')
                if user_role in role:
                    return func(*args, **kwargs)
                else:
                    return render_with_defaults("error.html", message="У вас нет прав на просмотр данной страницы.")
            else:
                return render_with_defaults("error.html", message="Вы не авторизированы. Авторизируйтесь для продолжения работы.")
        return wrap_in
    return wrap_out


# тут не передаём имя того, что проверяем, так как resourse_name будет передан уже при вызове функции, а не до этого
# resourse_name не может быть непосредственно передан в декоратор до того, как функция будет вызвана,
# потому что в момент декорирования Python ещё не знает значение этого параметра.
def role_required_stats(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = kwargs.get('resource_name')
        user_role = session.get('user_role')
        query_file = None
        if name:
            with open("data/query.json") as f:
                query_file = json.load(f)
            if request.blueprint == 'query_bp':
                if name in query_file[user_role]['table']:
                    return func(*args, **kwargs)
            elif request.blueprint == 'report_bp':
                if name in query_file[user_role]['report'] or name in query_file[user_role]['procedure']:
                    return func(*args, **kwargs)
            else:
                return render_with_defaults("error.html", message="У вас нет прав на просмотр данной страницы.")
        else:
            return render_with_defaults("error.html", message="Неизвестная ошибка.")
    return wrapper



