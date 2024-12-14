from flask import Blueprint, session, redirect, url_for, render_template, current_app, request
from access import role_required
from database.sql_provider import SQLProvider
import os
from datetime import date
from currency.model_route import get_currency_names, get_currency_rate, set_currency_rates

blueprint_currency = Blueprint('currency_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_currency.route('/')
def currency_index():
    currency_names = get_currency_names(current_app.config['db_config'], provider)
    if not currency_names.status:
        return render_template("error.html",
                               user_role=session.get('user_grop'),
                               message=currency_names.error_message)
    else:
        return render_template('currency_main.html',
                               user_role=session.get('user_group'),
                               url_prefix=blueprint_currency.url_prefix,
                               current_date=date.today().strftime("%d.%m.%Y"),
                               currencies=currency_names.result)


@blueprint_currency.route('/<currency>')
def show_rate(currency):
    rates = get_currency_rate(current_app.config['db_config'], provider, currency)
    currency_names = get_currency_names(current_app.config['db_config'], provider)
    if not rates.status:
        return render_template("error.html", message=rates.error_message)
    else:
        print(blueprint_currency.url_prefix)
        return render_template('currency_main.html',
                               user_role=session.get('user_group'),
                               current_date=date.today().strftime("%d.%m.%Y"),
                               currencies=currency_names.result,
                               rates=rates.result,
                               currency_cur=currency)


@blueprint_currency.route('/update', methods=['GET'])
@role_required(['admin'])
def currency_update_index():
    currency_names = get_currency_names(current_app.config['db_config'], provider)
    if not currency_names.status:
        return render_template("error.html",
                               user_role=session.get('user_grop'),
                               message=currency_names.error_message)
    else:
        return render_template("currency_set.html",
                               user_role=session.get('user_group'),
                               currencies=currency_names.result,
                               current_date=date.today().strftime("%d.%m.%Y"))


@blueprint_currency.route('/update', methods=['POST'])
@role_required(['admin'])
def currency_update_main():
    form = request.form
    result = set_currency_rates(current_app.config['db_config'], provider, form)
    if not result.status:
        return render_template("error.html",
                               user_role=session.get('user_group'),
                               message=result.error_message)
    else:
        return redirect(url_for('currency_bp.currency_index'))
