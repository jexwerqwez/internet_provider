import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from sqlalchemy import text
from database.connect import engine
from access import group_required, group_validation

blueprint_request = Blueprint('blueprint_request', __name__, template_folder='templates', static_folder='static')
current_dir = os.path.dirname(os.path.abspath(__file__))

def execute_query_from_file(filename, **params):
    with open(os.path.join(current_dir, 'sql', filename), 'r') as file:
        query = file.read().strip()
    with engine.connect() as connection:
        result = connection.execute(text(query).bindparams(**params))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]


def get_clients_name(client_name, page, per_page=10):
    offset = (page - 1) * per_page
    return execute_query_from_file('clients/search_by_name.sql', client_name=client_name, limit=per_page, offset=offset)


def get_clients_balance(min_balance, max_balance, page, per_page=10):
    offset = (page - 1) * per_page
    return execute_query_from_file('clients/search_by_balance.sql', min_balance=min_balance, max_balance=max_balance, limit=per_page, offset=offset)


@blueprint_request.route('/')
@group_required
def menu_detail():
    if group_validation(current_app.config['access_config'], 'blueprint_clients'):
        return render_template("clients/menu.html")
    elif group_validation(current_app.config['access_config'], 'blueprint_services'):
        return render_template("services/menu.html")
    else:
    # categories = get_categories()
        return render_template("menu.html")

@blueprint_request.route('/exit')
def exit_app():
    return render_template("main-menu.html")


@blueprint_request.route('/clinets_name_detail', methods=['GET', 'POST'])
@group_required
def client_name_detail():
    clients = []
    query = ""
    if request.method == 'POST':
        # product_name = "%" + request.form.get('product_name') + "%"
        client_name = request.form.get('client_name')
        clients = get_clients_name(client_name, page=1)
        query = client_name
    return render_template("clients/name_detail.html", clients=clients, query=query)

@blueprint_request.route('/balance_detail', methods=['GET', 'POST'])
@group_required
def client_balance_detail():
    clients = []
    min_balance = ""
    max_balance = ""
    current_page = 1
    if request.method == 'POST':
        min_balance = request.form.get('min_balance')
        max_balance = request.form.get('max_balance')
        clients = get_clients_balance(min_balance, max_balance, page=current_page)
    print(clients)
    return render_template("clients/balance_detail.html", clients=clients, min_balance=min_balance, max_balance=max_balance, current_page=current_page)


def get_service_cost(min_cost, max_cost, page, per_page=10):
    offset = (page - 1) * per_page
    return execute_query_from_file('services/search_by_cost.sql', min_cost=min_cost, max_cost=max_cost, limit=per_page, offset=offset)


@blueprint_request.route('/cost_detail', methods=['GET', 'POST'])
@group_required
def service_cost_detail():
    services = []
    min_cost = ""
    max_cost = ""
    current_page = 1
    if request.method == 'POST':
        min_cost = request.form.get('min_cost')
        max_cost = request.form.get('max_cost')
        services = get_service_cost(min_cost, max_cost, page=current_page)
    print(services)
    return render_template("services/cost_detail.html", services=services, min_cost=min_cost, max_cost=max_cost, current_page=current_page)


def get_services_name(name, page, per_page=10):
    offset = (page - 1) * per_page
    return execute_query_from_file('services/search_by_name.sql', name=name, limit=per_page, offset=offset)


def get_services_name(name, page, per_page=10):
    offset = (page - 1) * per_page
    return execute_query_from_file('services/search_by_name.sql', name=name, limit=per_page, offset=offset)


@blueprint_request.route('/services_name_detail', methods=['GET', 'POST'])
@group_required
def service_name_detail():
    services = []
    query = ""
    if request.method == 'POST':
        # product_name = "%" + request.form.get('product_name') + "%"
        name = request.form.get('name')
        services = get_services_name(name, page=1)
        query = name
    print(services)
    return render_template("services/name_detail.html", services=services, query=query)
