import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import text
from database.connect import engine
from access import group_required

blueprint_account = Blueprint('blueprint_account', __name__, template_folder='templates', static_folder='static')
current_dir = os.path.dirname(os.path.abspath(__file__))


def execute_query_from_file(filename, **params):
    with open(os.path.join(current_dir, 'sql', filename), 'r') as file:
        query = file.read().strip()
    with engine.connect() as connection:
        result = connection.execute(text(query).bindparams(**params))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]


def get_account_info(user_id):
    return execute_query_from_file('get_account_info.sql', user_id=user_id)


def get_contract_number(user_id):
    return execute_query_from_file('get_contract_number.sql', user_id=user_id)[0]['contract_number']


def get_balance_history():
    user_id = session.get('user_id')
    contract_number = get_contract_number(user_id)
    return execute_query_from_file('get_balance_history.sql', contract_number=contract_number)


def get_activated_services():
    user_id = session.get('user_id')
    contract_number = get_contract_number(user_id)
    return execute_query_from_file('get_activated_services.sql', contract_number=contract_number)


def get_status(user_id):
    contract_number = get_contract_number(user_id)
    status = execute_query_from_file('get_status.sql', contract_number=contract_number)[0]['service_status']
    return 'Активен' if status == 1 else 'Заблокирован'

@blueprint_account.route('/', methods=['GET', 'POST'])
@group_required
def account():
    user_id = session.get('user_id')
    if user_id:
        contract = get_account_info(user_id)
        status = get_status(user_id)
        print(contract)
        return render_template("account.html", contract=contract, status=status)
    else:
        return redirect(url_for('auth.start_auth'))


@blueprint_account.route('/balance-history', methods=['GET', 'POST'])
@group_required
def balance_history():
    balance_history_list = get_balance_history()
    return render_template("balance_history.html", balance_history_list=balance_history_list)


@blueprint_account.route('/activated-services', methods=['GET', 'POST'])
@group_required
def activated_services():
    activated_services_list = get_activated_services()
    return render_template("activated_services.html", activated_services=activated_services_list)
