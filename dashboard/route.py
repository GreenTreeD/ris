import os
from datetime import timedelta
from flask import Blueprint, session, redirect, url_for, current_app, request
from access import role_required
from dashboard.model_route import *
from database.sql_provider import SQLProvider
from utils.utils import render_with_defaults

blueprint_dashboard = Blueprint('dashboard_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_dashboard.route('/')
def dashboard_redirect():
    if session.get('user_group') == 'user':
        return redirect(url_for('dashboard_bp.d_user'))
    elif session.get('user_group') == 'admin':
        return redirect(url_for('dashboard_bp.d_admin'))
    elif session.get('user_group') == 'manager':
        return redirect(url_for('dashboard_bp.d_manager'))
    else:
        return redirect(url_for('main_menu'))


# Для группы пользователей user

@blueprint_dashboard.route('/user')
@role_required(['user'])
def d_user():
    user_info = getuserinfo(current_app.config['db_config'], provider, session.get('user_login'))
    if not user_info.status:
        return render_with_defaults("error.html",
                                    message=user_info.error_message)
    bills = getbills(current_app.config['db_config'],
                     provider,
                     current_app.config['cache_config'],
                     session.get('user_login'))
    if not bills.status:
        return render_with_defaults("error.html",
                                    message=bills.error_message)

    bill_history = gethistory(current_app.config['db_config'], provider, session.get('user_login'), "LIMIT 3")
    if not bill_history.status:
        return render_with_defaults("error.html",
                                    message=bill_history.error_message)

    bill_history_inner = getinnerhistory(current_app.config['db_config'], provider, session.get('user_login'),
                                         "LIMIT 3")
    if not bill_history_inner.status:
        return render_with_defaults("error.html",
                                    message=bill_history_inner.error_message)
    return render_with_defaults("dashboard.html",
                                user_login=session.get('user_login'),
                                user_info=user_info.result,
                                bills=bills.result,
                                bills_history=bill_history.result,
                                bills_history_inner=bill_history_inner.result)


@blueprint_dashboard.route('/user/history')
@role_required(['user'])
def d_user_history():
    bill_history = gethistory(current_app.config['db_config'], provider, session.get('user_login'))

    if not bill_history.status:
        return render_with_defaults("error.html", message=bill_history.error_message)
    return render_with_defaults("dashboard_user_history.html",
                                bill_history=bill_history.result,
                                type="outer")


@blueprint_dashboard.route('/user/inner_history')
@role_required(['user'])
def d_user_history_inner():
    bill_history = getinnerhistory(current_app.config['db_config'], provider, session.get('user_login'))
    if not bill_history.status:
        return render_with_defaults("error.html",
                                    message=bill_history.error_message)
    return render_with_defaults("dashboard_user_history.html",
                                bill_history=bill_history.result,
                                type="inner")


@blueprint_dashboard.route('/user/statistics', methods=["GET", "POST"])
@role_required(['user'])
def statistics_user_index():
    if request.method == "GET":
        begin_date = (date.today() - timedelta(days=10)).isoformat()
        end_date = date.today().isoformat()
    else:
        begin_date = request.form.get('begin_date')
        end_date = request.form.get('end_date')

    detalisation_bills = getbilldetalisation(current_app.config['db_config'], provider,
                                             session.get('user_login'), begin_date, end_date)
    if not detalisation_bills.status:
        return render_with_defaults("error.html",
                                    message=detalisation_bills.error_message)

    detalisation_bills_inner = getbilldetalisationinner(current_app.config['db_config'], provider,
                                                        session.get('user_login'), begin_date, end_date)
    if not detalisation_bills_inner.status:
        return render_with_defaults("error.html",
                                    message=detalisation_bills_inner.error_message)

    return render_with_defaults("statistics.html",
                                begin_date=begin_date,
                                end_date=end_date,
                                detalisation_bills=detalisation_bills.result,
                                detalisation_bills_inner=detalisation_bills_inner.result)


@blueprint_dashboard.route('/user/newbill', methods=["GET"])
@role_required(['user'])
def d_user_new_bill():
    currencies = getcurrencies(current_app.config['db_config'], provider)
    if not currencies.status:
        return render_with_defaults("error.html",
                                    message=currencies.error_message)
    return render_with_defaults("new_bill.html",
                                user_login=session.get('user_login'),
                                currencies=currencies.result)


@blueprint_dashboard.route('/user/newbill', methods=["POST"])
@role_required(['user'])
def d_user_new_bill_main():
    result = newbill(current_app.config['db_config'], provider, request.form)
    if not result.status:
        return render_with_defaults("error.html",
                                    message=result.error_message)
    return render_with_defaults("message.html",
                                header="Успех",
                                message="Счёт был успешно создан, проверьте свой личный кабинет.")


@blueprint_dashboard.route('/user/transfer_menu')
@role_required(['user'])
def d_user_transfer_menu():
    return render_with_defaults("transfer.html", type="menu")


@blueprint_dashboard.route('/user/transfer_menu/transfer_outer', methods=['GET'])
@role_required(['user'])
def d_user_transfer_outer():
    bills = getbills(current_app.config['db_config'],
                     provider,
                     current_app.config['cache_config'],
                     session.get('user_login'))
    if not bills.status:
        return render_with_defaults("error.html", message=bills.error_message)
    return render_with_defaults("transfer.html",
                                type="outer",
                                sender_login=session.get('user_login'),
                                bills=bills.result)


@blueprint_dashboard.route('/user/transfer_menu/transfer_inner', methods=['GET'])
@role_required(['user'])
def d_user_transfer_inner():
    bills = getbills(current_app.config['db_config'],
                     provider,
                     current_app.config['cache_config'],
                     session.get('user_login'))
    if not bills.status:
        return render_with_defaults("error.html",
                                    message=bills.error_message)
    return render_with_defaults("transfer.html",
                                type="inner",
                                sender_login=session.get('user_login'),
                                bills=bills.result)


@blueprint_dashboard.route('/user/transfer_menu/transfer_outer', methods=['POST'])
@blueprint_dashboard.route('/user/transfer_menu/transfer_inner', methods=['POST'])
@role_required(['user'])
def d_user_transfer_POST():
    if request.form.get('receiver_login'):
        receiver_bill = findbill(current_app.config['db_config'], provider,
                                 [request.form.get('receiver_login'), request.form.get('sender_bill')])
        if not receiver_bill.status:
            return render_with_defaults("error.html",
                                        message=receiver_bill.error_message)
        user_data = dict(request.form)
        user_data['receiver_bill'] = receiver_bill.result
    else:
        if request.form.get('receiver_bill') == request.form.get('sender_bill'):
            return render_with_defaults("error.html",
                                        message="Отправляющий и принимающий счета совпадают.")
        user_data = request.form

    result = transfer(current_app.config['db_config'], provider, user_data)
    if not result.status:
        return render_with_defaults("error.html",
                                    message=result.error_message)
    return render_with_defaults("message.html",
                                header="Успех",
                                message="Перевод был успешно зачислен.")


# Для группы пользователей admin

@blueprint_dashboard.route('/admin')
@role_required(['admin'])
def d_admin():
    user_info = getworkerinfo(current_app.config['db_config'], provider, session.get('user_login'))
    if not user_info.status:
        return render_with_defaults("error.html",
                                    message=user_info.error_message)

    return render_with_defaults("dashboard.html",
                                user_login=session.get('user_login'),
                                user_info=user_info.result)


# Для группы пользователей manager

@blueprint_dashboard.route('/manager')
@role_required(['manager'])
def d_manager():
    user_info = getworkerinfo(current_app.config['db_config'], provider, session.get('user_login'))
    if not user_info.status:
        return render_with_defaults("error.html",
                                    message=user_info.error_message)
    return render_with_defaults("dashboard.html",
                                user_login=session.get('user_login'),
                                user_info=user_info.result)


@blueprint_dashboard.route('/manager/deposit', methods=['POST', 'GET'])
@role_required(['manager'])
def d_manager_deposit():
    if request.method == 'GET':
        return render_with_defaults("manager_route.html", type="deposit")
    else:
        user_data = request.form
        result = deposit_manager(current_app.config['db_config'], provider, user_data, session.get('user_login'))
        if not result.status:
            return render_with_defaults("error.html", message=result.error_message)
        return render_with_defaults("message.html", header="Успешное зачисление", message="Проверьте целевой счёт.")


@blueprint_dashboard.route('/manager/withdraw', methods=['POST', 'GET'])
@role_required(['manager'])
def d_manager_withdraw():
    if request.method == 'GET':
        return render_with_defaults("manager_route.html", type="withdraw")
    else:
        user_data = request.form
        result = deposit_manager(current_app.config['db_config'], provider, user_data, session.get('user_login'))
        if not result.status:
            return render_with_defaults("error.html", message=result.error_message)
        return render_with_defaults("message.html", header="Успешное снятие", message="Проверьте целевой счёт.")


@blueprint_dashboard.route('/manager/client', methods=['POST', 'GET'])
@role_required(['manager'])
def d_manager_info():
    if request.method == 'GET':
        return render_with_defaults("user_info.html", type="GET")
    else:
        user_info = getuserinfo(current_app.config['db_config'], provider, request.form.get('login'))
        if not user_info.status:
            return render_with_defaults("error.html",
                                        message=user_info.error_message)
        session['client_login'] = user_info.result[6]

        bills = getbills(current_app.config['db_config'],
                         provider,
                         current_app.config['cache_config'],
                         user_info.result[6])

        if not bills.status:
            return render_with_defaults("error.html",
                                        message=bills.error_message)
        return render_with_defaults("user_info.html", type="POST",
                                    user_info=user_info.result,
                                    bills=bills.result)


@blueprint_dashboard.route('/manager/exit', methods=['POST', 'GET'])
@role_required(['manager'])
def d_manager_exit():
    if session.get('client_login',''):
        session.pop('client_login')
        return render_with_defaults("message.html",
                                    title="До свидания",
                                    message="Работа с клиентом закончена.")
    else:
        return render_with_defaults("error.html",
                                    message="Работа с клиентом не начата.")



