import json
from flask import Flask, render_template, session, redirect, url_for
from sqlalchemy.orm import declarative_base
from blueprints.auth.auth import auth
from blueprints.blueprint_services.route import blueprint_services
from blueprints.blueprint_request.route import blueprint_request
from blueprints.blueprint_report.route import blueprint_report
from blueprints.blueprint_account.route import blueprint_account
from blueprints.blueprint_clients.route import blueprint_clients
from blueprints.blueprint_management.route import blueprint_management
from blueprints.blueprint_constructor.route import blueprint_constructor

from access import login_required, group_required

app = Flask(__name__)
app.secret_key = 'ChinChanChon'
Base = declarative_base()

app.register_blueprint(blueprint_request, url_prefix='/requests')
app.register_blueprint(blueprint_account, url_prefix='/account')
app.register_blueprint(blueprint_services, url_prefix='/services')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_clients, url_prefix='/clients')
app.register_blueprint(blueprint_management, url_prefix='/management')
app.register_blueprint(blueprint_constructor, url_prefix='/constructor')
app.register_blueprint(auth, url_prefix='/auth')

app.config['access_config'] = json.load(open('data_files/access.json'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def menu_choice():
    user_group = session.get('user_group', 'typical')
    if 'user_id' in session:
        if session.get('user_group') is None or session.get('user_group') == 'typical':
            return render_template('external_user_menu.html')
        else:
            return render_template('internal_user_menu.html', user_group=user_group)
    else:
        redirect(url_for('auth.start_auth'))

@app.route('/exit')
@login_required
def exit_app():
    session.clear()
    return render_template("exit.html")

# @app.route('/admin_only')
# @login_required
# @group_required
# def blueprint_services():
#     return render_template('admin_only.html')
#

if __name__ == "__main__":
    app.run()
