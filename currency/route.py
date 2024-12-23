from flask import Blueprint, redirect, url_for, current_app, request
from access import role_required
from database.sql_provider import SQLProvider
import os
from currency.model_route import *
from utils.utils import render_with_defaults

blueprint_currency = Blueprint('currency_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_currency.route('/')
def currency_index():
    currency_names = get_currency_names(current_app.config['db_config'], provider)
    if not currency_names.status:
        return render_with_defaults("error.html",
                                    message=currency_names.error_message)
    else:
        return render_with_defaults('currency_main.html',
                                    url_prefix=blueprint_currency.url_prefix,
                                    current_date=date.today().strftime("%d.%m.%Y"),
                                    currencies=currency_names.result)


@blueprint_currency.route('/<currency>')
def show_rate(currency):
    rates = get_currency_rate(current_app.config['db_config'], provider, currency)
    currency_names = get_currency_names(current_app.config['db_config'], provider)
    if not rates.status:
        return render_with_defaults("error.html", message=rates.error_message)
    else:

        return render_with_defaults('currency_main.html',
                                    current_date=date.today().strftime("%d.%m.%Y"),
                                    currencies=currency_names.result,
                                    rates=rates.result,
                                    currency_cur=currency)


@blueprint_currency.route('/update', methods=['GET'])
@role_required(['admin'])
def currency_update_index():
    currency_names = get_currency_names(current_app.config['db_config'], provider)
    if not currency_names.status:
        return render_with_defaults("error.html",
                                    message=currency_names.error_message)
    else:
        return render_with_defaults("currency_set.html",
                                    currencies=currency_names.result,
                                    current_date=date.today().strftime("%d.%m.%Y"))


@blueprint_currency.route('/update', methods=['POST'])
@role_required(['admin'])
def currency_update_main():
    form = request.form
    result = set_currency_rates(current_app.config['db_config'], provider, form)
    if not result.status:
        return render_with_defaults("error.html",
                                    message=result.error_message)
    else:
        return redirect(url_for('currency_bp.currency_index'))
