from functools import wraps
from flask import session, render_template


def login_required(func):
    @wraps(func)
    def wrapper(*argc, **kwargs):
        if 'user_login' in session:
            return func(*argc, **kwargs)
        else:
            return render_template("error.html",
                                   user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                                   message="Вы не авторизированы.Авторизируйтесь для продолжения работы.")
    return wrapper


def role_required(role: list):
    def wrap_out(func):
        @wraps(func)
        def wrap_in(*args, **kwargs):
            if 'user_group' in session:
                user_role = session.get('user_group')
                if user_role in role:
                    return func(*args, **kwargs)
                else:
                    return render_template("error.html",
                                           user_role=(session.get('user_group')if session.get('user_group') else 'unauth'),
                                           message="У вас нет прав на просмотр данной страницы.")
            else:
                return render_template("error.html",
                                       user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                                       message="Вы не авторизированы. Авторизируйтесь для продолжения работы.")

        return wrap_in

    return wrap_out
