from flask import Blueprint, session, redirect, url_for, render_template, current_app, request
from access import role_required
from database.sql_provider import SQLProvider
from dashboard.model_route import *
import os
from datetime import date, timedelta

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
        return render_template("error.html",
                               user_role=session.get('user_group'),
                               message=user_info.error_message)

    bills = getbills(current_app.config['db_config'], provider, session.get('user_login'))
    if not bills.status:
        return render_template("error.html",
                               user_role=session.get('user_group'),
                               message=bills.error_message)

    bill_history = gethistory(current_app.config['db_config'], provider, session.get('user_login'), "LIMIT 5")
    if not bill_history.status:
        return render_template("error.html",
                               user_role=session.get('user_group'),
                               message=bill_history.error_message)

    bill_history_inner = getinnerhistory(current_app.config['db_config'], provider, session.get('user_login'),
                                         "LIMIT 5")
    if not bill_history_inner.status:
        return render_template("error.html",
                               user_role=session.get('user_group'),
                               message=bill_history_inner.error_message)

    return render_template("dashboard.html",
                           user_role=session.get('user_group'),
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
        return render_template("error.html",
                               user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                               message=bill_history.error_message)
    return render_template("dashboard.html",
                           user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                           bill_history=bill_history,
                           type="outer")


@blueprint_dashboard.route('/user/inner_history')
@role_required(['user'])
def d_user_history_inner():
    bill_history = getinnerhistory(current_app.config['db_config'], provider, session.get('user_login'))
    if not bill_history.status:
        return render_template("error.html",
                               user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                               message=bill_history.error_message)
    return render_template("dashboard.html",
                           user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                           bill_history=bill_history,
                           type="inner")


@blueprint_dashboard.route('/user/history/<bill_id>+<change_date>')
@role_required(['user'])
def d_user_bill(bill_id, change_date):
    bill_history = gethistorydetails(current_app.config['db_config'], provider,
                                     bill_id, change_date)
    if not bill_history.status:
        return render_template("error.html",
                               user_role=session.get('user_group'),
                               message=bill_history.error_message)
    return render_template("transfer_detalisation.html",
                           user_role=session.get('user_group'),)


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
        return render_template("error.html",
                               user_role=session.get('user_group'),
                               message=detalisation_bills.error_message)

    detalisation_bills_inner = getbilldetalisationinner(current_app.config['db_config'], provider,
                                                        session.get('user_login'), begin_date, end_date)
    if not detalisation_bills_inner.status:
        return render_template("error.html",
                               user_role=session.get('user_group'),
                               message=detalisation_bills_inner.error_message)

    return render_template("statistics.html",
                           user_role=session.get('user_group'),
                           begin_date=begin_date,
                           end_date=end_date,
                           detalisation_bills=detalisation_bills.result,
                           detalisation_bills_inner=detalisation_bills_inner.result)


@blueprint_dashboard.route('/user/newbill', methods=["GET"])
@role_required(['user'])
def d_user_new_bill():
    currencies = getcurrencies(current_app.config['db_config'], provider)
    if not currencies.status:
        return render_template("error.html",
                               user_role=(session.get('user_group')if session.get('user_group') else 'unauth'),
                               message=currencies.error_message)
    return render_template("new_bill.html",
                           user_role=(session.get('user_group')if session.get('user_group') else 'unauth'),
                           user_login=session.get('user_login'),
                           currencies=currencies.result)


@blueprint_dashboard.route('/user/newbill', methods=["POST"])
@role_required(['user'])
def d_user_new_bill_main():
    result = newbill(current_app.config['db_config'], provider, request.form)
    if not result.status:
        return render_template("error.html",
                               user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                               message=result.error_message)
    return render_template("message.html",
                           user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                           header="Успех",
                           message="Счёт был успешно создан, проверьте свой личный кабинет.")


@blueprint_dashboard.route('/user/transfer_menu')
@role_required(['user'])
def d_user_transfer_menu():
    return render_template("transfer.html",
                           user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                           type="menu")


@blueprint_dashboard.route('/user/transfer_menu/transfer_outer', methods=['GET'])
@role_required(['user'])
def d_user_transfer_outer():
    bills = getbills(current_app.config['db_config'], provider, session.get('user_login'))
    if not bills.status:
        return render_template("error.html",
                               user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                               message=bills.error_message)
    return render_template("transfer.html",
                           user_role=session.get('user_group'),
                           type="outer",
                           sender_login=session.get('user_login'),
                           bills=bills.result)


@blueprint_dashboard.route('/user/transfer_menu/transfer_inner', methods=['GET'])
@role_required(['user'])
def d_user_transfer_inner():
    bills = getbills(current_app.config['db_config'], provider, session.get('user_login'))
    if not bills.status:
        return render_template("error.html",
                               user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                               message=bills.error_message)
    return render_template("transfer.html",
                           user_role=session.get('user_group'),
                           type="inner",
                           sender_login=session.get('user_login'),
                           bills=bills.result)


@blueprint_dashboard.route('/user/transfer_menu/transfer_outer', methods=['POST'])
@blueprint_dashboard.route('/user/transfer_menu/transfer_inner', methods=['POST'])
@role_required(['user'])
def d_user_transfer_POST():
    print(request.form)
    if request.form.get('receiver_login'):
        receiver_bill = findbill(current_app.config['db_config'], provider,
                                 [request.form.get('receiver_login'), request.form.get('sender_bill')])
        if not receiver_bill.status:
            return render_template("error.html",
                                   user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                                   message=receiver_bill.error_message)
        user_data = dict(request.form)
        user_data['receiver_bill'] = receiver_bill.result
    else:
        if request.form.get('receiver_bill') == request.form.get('sender_bill'):
            return render_template("error.html",
                                   user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                                   message="Отправляющий и принимающий счета совпадают.")

        user_data = request.form

    result = transfer(current_app.config['db_config'], provider, user_data)
    if not result.status:
        return render_template("error.html",
                               user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                               message=result.error_message)
    return render_template("message.html",
                           user_role=session.get('user_group'),
                           header="Успех",
                           message="Перевод был успешно зачислен.")


# Для группы пользователей admin

@blueprint_dashboard.route('/admin')
@role_required(['admin'])
def d_admin():
    user_info = getworkerinfo(current_app.config['db_config'], provider, session.get('user_login'))
    if not user_info.status:
        return render_template("error.html",
                               user_role=(session.get('user_group') if session.get('user_group') else 'unauth'),
                               message=user_info.error_message)

    return render_template("dashboard.html",
                           user_role=session.get('user_group'),
                           user_login=session.get('user_login'),
                           user_info=user_info.result)


# Для группы пользователей manager

@blueprint_dashboard.route('/manager')
@role_required(['manager'])
def d_manager():
    return "Личный кабинет менеджера"


@blueprint_dashboard.route('/manager/new_bill')
@role_required(['manager'])
def d_manager_new_bill():
    return "Оформление нового счёта от лица менеджера"


@blueprint_dashboard.route('/manager/transfer')
@role_required(['manager'])
def d_manager_transfer():
    return "Перевод другому пользователю"


@blueprint_dashboard.route('/manager/transfer_inner')
@role_required(['manager'])
def d_manager_transfer_inner():
    return "Перевод пользователю"


@blueprint_dashboard.route('/manager/deposit')
@role_required(['manager'])
def d_manager_deposit():
    return "Зачисление"


@blueprint_dashboard.route('/manager/withdraw')
@role_required(['manager'])
def d_manager_withdraw():
    return "Снятие"
