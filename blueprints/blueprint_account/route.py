import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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
    result = execute_query_from_file('get_contract_number.sql', user_id=user_id)
    if result:
        return result[0]['contract_number']
    else:
        return None  # или другое подходящее значение по умолчанию


def get_balance_history():
    user_id = session.get('user_id')
    contract_number = get_contract_number(user_id)
    return execute_query_from_file('get_balance_history.sql', contract_number=contract_number)


def get_balance():
    user_id = session.get('user_id')
    contract_number = get_contract_number(user_id)
    return execute_query_from_file('get_current_balance.sql', contract_number=contract_number)


def get_activated_services():
    user_id = session.get('user_id')
    contract_number = get_contract_number(user_id)
    return execute_query_from_file('get_activated_services.sql', contract_number=contract_number)


def get_status(user_id):
    contract_number = get_contract_number(user_id)
    status = execute_query_from_file('get_status.sql', contract_number=contract_number)[0]['service_status']
    return 'Активен' if status == 1 else 'Заблокирован'


@blueprint_account.route('/replenish_balance', methods=['GET', 'POST'])
@group_required
def replenish_balance():
    user_id = session.get('user_id')
    contract_number = get_contract_number(user_id)
    balance_data = get_balance()  # Получение данных о балансе
    balance = balance_data[0]['current_balance'] if balance_data else 0  # Извлечение числа
    message = ""

    if request.method == 'POST':
        cash = request.form.get('cash')
        if cash:
            try:
                with engine.connect() as connection:
                    connection.execute(text("CALL replenish_balance(:contract_number, :cash)"), {'contract_number': contract_number, 'cash': cash})
                    connection.commit()
                balance_data = get_balance()  # Обновление данных о балансе
                balance = balance_data[0]['current_balance'] if balance_data else 0  # Обновление числа
                message = "Ваш баланс пополнен на " + str(cash) + " руб."
            except Exception as e:
                print("Ошибка при пополнении баланса:", e)
                return render_template("error_message.html",
                                       message="Невозможно пополнить баланс. Пожалуйста, попробуйте позже.")

    return render_template("replenish_balance.html", balance=balance, message=message)


@blueprint_account.route('/', methods=['GET', 'POST'])
@group_required
def account():
    user_id = session.get('user_id')
    print("aboba id", user_id)
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
