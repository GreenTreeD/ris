

from flask import Flask, render_template, session, json, redirect, url_for
from auth.route import blueprint_auth
from currency.route import blueprint_currency
from dashboard.route import blueprint_dashboard


app = Flask(__name__)
with open("data/dbconfig.json") as f:
    app.config['db_config'] = json.load(f)


app.secret_key = 'You will never guess'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_currency, url_prefix='/currency')
app.register_blueprint(blueprint_dashboard, url_prefix='/dashboard')


@app.route('/')
def main_menu():
    user_role = "unauth"
    if 'user_group' in session:
        user_role = session.get('user_group')

    print(user_role)
    return render_template('main_menu.html', user_role=user_role)


@app.route('/exit')
def exit_func():
    if 'user_group' in session:
        session.clear()
        return render_template('logout.html', user_role=(session.get('user_role')if session.get('user_role') else 'unauth'))
    return redirect(url_for('main_menu'))


@app.route('/error')
def error_message():
    return render_template("error.html", message="Какая-то ошибка :(", user_role=(session.get('user_role')if session.get('user_role') else 'unauth'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="404 Not Found. Данной страницы не существует."), 404


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5002, debug=True)


