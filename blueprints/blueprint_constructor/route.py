import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import text
from database.connect import engine
from access import group_required

blueprint_constructor = Blueprint('blueprint_constructor', __name__, template_folder='templates', static_folder='static')
current_dir = os.path.dirname(os.path.abspath(__file__))

def execute_query_from_file(filename, **params):
    with open(os.path.join(current_dir, 'sql', filename), 'r') as file:
        query = file.read().strip()
    with engine.connect() as connection:
        result = connection.execute(text(query).bindparams(**params))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]


def get_contract_number(user_id):
    result = execute_query_from_file('get_contract_number.sql', user_id=user_id)
    if result:  # Проверка, что результат не пуст
        return result[0]['contract_number']
    else:
        return render_template("error_message.html", message="Произошла ошибка при выполнении транзакции. Пожалуйста, попробуйте позже.")


def count_services():
    with open(os.path.join(current_dir, 'sql/count_services.sql'), 'r') as file:
        query = file.read().strip()
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchone()[0]


def get_services_by_name(product_name, page, per_page=10):
    offset = (page - 1) * per_page
    return execute_query_from_file('search_by_name.sql', product_name=product_name, limit=per_page, offset=offset)


def get_services_by_price(min_price, max_price, page, per_page=10):
    offset = (page - 1) * per_page
    return execute_query_from_file('search_by_price.sql', min_price=min_price, max_price=max_price, limit=per_page, offset=offset)


def get_all_from_db(page, per_page=10):
    offset = (page - 1) * per_page
    return execute_query_from_file('get_all_services.sql', limit=per_page, offset=offset)


def get_activated_services():
    user_id = session.get('user_id')
    contract_number = get_contract_number(user_id)
    return execute_query_from_file('get_activated_services.sql', contract_number=contract_number)


def get_unactivated_services():
    user_id = session.get('user_id')
    contract_number = get_contract_number(user_id)
    return execute_query_from_file('get_unactivated_services.sql', contract_number=contract_number)


def get_service_by_id(all_services_id):
    result = execute_query_from_file('get_service_by_id.sql', all_services_id=all_services_id)
    if result:
        return result[0]  # Возвращаем первый элемент списка
    return None


@blueprint_constructor.route('/activate-service', methods=['POST'])
def activate_service():
    return redirect(url_for('blueprint_constructor.all_services'))

@blueprint_constructor.route('/deactivate-service', methods=['POST'])
def deactivate_service():
    return redirect(url_for('blueprint_constructor.all_services'))


def get_all_services_grouped_by_type(page, per_page=10):
    offset = (page - 1) * per_page
    services = execute_query_from_file('get_all_services.sql', limit=per_page, offset=offset)
    grouped_services = {}
    for service in services:
        service_type = service['type']
        if service_type not in grouped_services:
            grouped_services[service_type] = []
        grouped_services[service_type].append(service)
    return grouped_services


@blueprint_constructor.route('/', methods=['GET', 'POST'])
@group_required
def all_services():
    activated_services = [service['all_services_id'] for service in get_activated_services()]
    unactivated_services = [service['all_services_id'] for service in get_unactivated_services()]
    if 'clear_cart' in request.args:
        session.pop('basket', None)
        session.pop('total_cost', None)

    if request.method == 'POST':
        service_statuses = request.form.to_dict(flat=False)
        service_status_dict = {key.split('[')[1].split(']')[0]: value[0] for key, value in service_statuses.items() if key.startswith('service_status')}

        session['basket'] = {}
        total_cost = 0

        if service_status_dict:
            for service_id, status in service_status_dict.items():
                service_details = get_service_by_id(service_id)
                if service_details and status in ['1', '2']:
                    action = 'Подключение' if status == '1' else 'Отключение'
                    session['basket'][service_id] = {
                        'name': service_details['name'],
                        'cost': service_details['cost'],
                        'amount': 1,
                        'action': action
                    }
                    if status == '1':  # Учитываем стоимость только для подключаемых услуг
                        total_cost += service_details['cost']

            session['total_cost'] = total_cost
            session.modified = True

            return redirect(url_for('blueprint_constructor.order_details'))
        else:
            print("Нет данных о статусе услуг")
            return redirect(url_for('blueprint_constructor.order_details'))
    else:
        page = int(request.args.get('page', 1))
        total_products = count_services()
        total_pages = -(-total_products // 10)
        services_grouped_by_type = get_all_services_grouped_by_type(page)
        type_names = {'internet': 'Интернет', 'entertainment': 'Развлечения', 'services': 'Дополнительные услуги'}
        basket = session.get('basket', {})
        print(basket)

        return render_template("constructor.html", services_grouped_by_type=services_grouped_by_type,
                               type_names=type_names, current_page=page, total_pages=total_pages, basket=basket,
                               activated_services=activated_services, unactivated_services=unactivated_services)


@blueprint_constructor.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    internet_service_id = request.form.get('internet_service')
    other_services_ids = request.form.getlist('other_services[]')
    all_services_id = [internet_service_id] + other_services_ids
    total_cost = 0

    if 'basket' not in session:
        session['basket'] = {}

    for service_id in all_services_id:
        service_details = get_service_by_id(service_id)
        if not service_details:
            continue

        session['basket'][service_id] = {
            'name': service_details['name'],
            'cost': service_details['cost'],
            'amount': 1
        }
        total_cost += service_details['cost']

    session['total_cost'] = total_cost
    session.modified = True

    return redirect(url_for('blueprint_constructor.order_details'))


@blueprint_constructor.route('/order-details', methods=['GET', 'POST'])
def order_details():
    if 'clear_cart' in request.args:
        session.pop('basket', None)
        session.pop('total_cost', None)
        return redirect(url_for('blueprint_constructor.all_services'))

    if request.method == 'POST':
        return render_template('order.html')
    else:
        if 'basket' in session and session['basket']:
            basket_items = session['basket'].values()
            total_cost = session.get('total_cost', 0)
            return render_template('order.html', basket_items=basket_items, total_cost=total_cost)
    return render_template('order.html')
    # return redirect(url_for('blueprint_constructor.all_services'))


@blueprint_constructor.route('/clear-cart', methods=['POST'])
def clear_cart():
    session.pop('basket', None)
    session.pop('total_cost', None)
    session.modified = True
    return redirect(url_for('blueprint_constructor.all_services'))


@blueprint_constructor.route('/connect-tariff', methods=['POST'])
def connect_tariff():
    user_id = session.get('user_id')

    if 'basket' in session and session['basket']:
        with engine.connect() as connection:
            trans = connection.begin()  # Начало транзакции
            try:
                for service_id, service in session['basket'].items():
                    contract_number = get_contract_number(user_id)
                    params = {
                        'service_id': service_id,
                        'contract_id': contract_number,
                        'status': '1' if service['action'] == 'Подключение' else '2'
                    }
                    connection.execute(text("CALL AddServiceOnOff(:service_id, :contract_id, :status)"), params)
                trans.commit()  # Явный коммит транзакции
            except Exception as e:
                trans.rollback()  # Откат транзакции в случае ошибки
                return render_template("error_message.html", message="Произошла ошибка при выполнении транзакции. Пожалуйста, попробуйте позже.")

    # Очистка корзины и обновление сессии
    session.pop('basket', None)
    session.pop('total_cost', None)
    session.modified = True

    return render_template("tariff_connected.html")


@blueprint_constructor.route('/exit')
def exit_app():
    return render_template("main-menu.html")
