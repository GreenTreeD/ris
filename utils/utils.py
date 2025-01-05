from flask import render_template, session
from datetime import datetime


def render_with_defaults(template_name, **kwargs): #обертка для функции render_template чтобы не передавать роль пользователя
    default_context = {
        'user_role': session.get('user_role', 'unauth'),
        'client_login': session.get('client_login', '')
    }
    context = {**default_context, **kwargs}
    return render_template(template_name, **context)


def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object is not datetime")


def datetime_deserializer(dct):
    for key, value in dct.items():
        if isinstance(value, str):
            try:
                dct[key] = datetime.fromisoformat(value)
            except ValueError:
                pass
    return dct
