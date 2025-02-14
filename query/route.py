
import os
from flask import Blueprint, current_app, request, session
from access import role_required, role_required_stats
from query.model_route import *
from database.sql_provider import SQLProvider
from utils.utils import render_with_defaults
from datetime import date


blueprint_query = Blueprint('query_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/', methods=['GET'])
@role_required(['manager', 'admin'])
def query_index():
    table = generate_menu_list(session.get('user_role'), 'table')
    return render_with_defaults("menu.html", type='table', list=table)


@blueprint_query.route('/<resource_name>', methods=['POST', 'GET'])
@role_required(['manager', 'admin'])
@role_required_stats
def query_table(resource_name):
    if request.method == 'POST':
        user_data = {key: value for key, value in request.form.items() if value}
        tmp = show_resource(current_app.config['db_config'], provider, resource_name, user_data)
    else:
        tmp = show_resource(current_app.config['db_config'], provider, resource_name)
    if not tmp.status:
        return render_with_defaults("error.html", message=tmp.error_message)
    return render_with_defaults("resource_template.html",
                                name=tmp.result[0],
                                header=tmp.result[1],
                                content=tmp.result[2],
                                filtermenu=tmp.result[3])
