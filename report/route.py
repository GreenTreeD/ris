
import os
from flask import Blueprint, current_app, request, session, redirect, url_for
from access import role_required, role_required_stats
from report.model_route import *
from database.sql_provider import SQLProvider
from utils.utils import render_with_defaults
from datetime import date


blueprint_report = Blueprint('report_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['POST','GET'])
@role_required(['manager', 'admin'])
def report_index():
    report = generate_menu_list(session.get('user_role'), 'report')
    return render_with_defaults("menu.html", type='report', list=report)


@blueprint_report.route('/<resource_name>', methods=['POST', 'GET'])
@role_required(['manager', 'admin'])
@role_required_stats
def report_main(resource_name):
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
                                filtermenu=tmp.result[3],
                                type='report',
                                resource_name=resource_name)


@blueprint_report.route('/<resource_name>/create', methods=['POST', 'GET'])
@role_required(['manager', 'admin'])
@role_required_stats
def report_create(resource_name):
    if request.method == 'GET':
        name = generate_name(resource_name)
        curdate = date.today()
        return render_with_defaults("report_template.html",
                                    name=name,
                                    curdate=curdate)
    else:
        user_data = request.form
        res = create_report(current_app.config['db_config'], ('create_'+resource_name), user_data)
        if not res.status:
            return render_with_defaults("error.html", message=res.error_message)
        return redirect(url_for('report_bp.report_main', resource_name=resource_name))


