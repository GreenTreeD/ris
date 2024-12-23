

from flask import Flask, session, json, redirect, url_for
from auth.route import blueprint_auth
from currency.route import blueprint_currency
from dashboard.route import blueprint_dashboard
from query.route import blueprint_query
from utils.utils import render_with_defaults


app = Flask(__name__)
with open("data/dbconfig.json") as f:
    app.config['db_config'] = json.load(f)


app.secret_key = 'You will never guess'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_currency, url_prefix='/currency')
app.register_blueprint(blueprint_dashboard, url_prefix='/dashboard')
app.register_blueprint(blueprint_query, url_prefix='/query')


@app.route('/')
def main_menu():
    return render_with_defaults('main_menu.html')


@app.route('/exit')
def exit_func():
    if 'user_role' in session:
        session.clear()
        return render_with_defaults('logout.html')
    return redirect(url_for('main_menu'))


@app.route('/error')
def error_message():
    return render_with_defaults("error.html", message="Какая-то ошибка :(")


@app.errorhandler(404)
def page_not_found(e):
    return render_with_defaults('error.html', message="404 Not Found. Данной страницы не существует."), 404


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5002, debug=True)

