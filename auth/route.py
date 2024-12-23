from flask import Blueprint, session, redirect, url_for, current_app, request
from access import role_required
from database.sql_provider import SQLProvider
import os
from auth.model_route import auth, exist_check, reg_new
from utils.utils import render_with_defaults

blueprint_auth = Blueprint('auth_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET'])
def auth_index():
    return render_with_defaults('auth.html')


@blueprint_auth.route('/', methods=['POST'])
def auth_main():
    user_data = request.form
    res_info = auth(current_app.config['db_config'], user_data, provider)
    if not res_info.status:
        return render_with_defaults('error.html',

                                    message="Ошибка сервера")
    if not res_info.result:
        return render_with_defaults('error.html',

                                    message="Такой пользователь не существует")
    session['user_role'] = res_info.result[1]
    session['user_login'] = res_info.result[0]
    return redirect(url_for('main_menu'))


@blueprint_auth.route('/registration', methods=['GET'])
@role_required(['manager', 'admin'])
def registration_index():
    if session.get('user_role') == 'manager':
        return render_with_defaults('reg_manager.html')
    return render_with_defaults('reg_admin.html')


@blueprint_auth.route('/registration', methods=['POST'])
@role_required(['manager', 'admin'])
def registration_main():
    user_data = request.form
    res_info = exist_check(current_app.config['db_config'], user_data, provider)
    if not res_info.status:
        return render_with_defaults('error.html',
                                    message=res_info.error_message)

    res_info = reg_new(current_app.config['db_config'], user_data, provider)
    if not res_info.status:
        return render_with_defaults('error.html',

                                    message=res_info.error_message)
    return render_with_defaults("message.html", title="Успех",
                                message="Пользователь зарегистрирован. Вы можете перейти к авторизации.")
