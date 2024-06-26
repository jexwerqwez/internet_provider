import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import text
from database.connect import engine
from access import group_required

blueprint_services = Blueprint('blueprint_services', __name__, template_folder='templates', static_folder='static')
current_dir = os.path.dirname(os.path.abspath(__file__))

def execute_query_from_file(filename, **params):
    with open(os.path.join(current_dir, 'sql', filename), 'r') as file:
        query = file.read().strip()
    with engine.connect() as connection:
        result = connection.execute(text(query).bindparams(**params))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]


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


def get_service_by_id(all_services_id):
    result = execute_query_from_file('get_service_by_id.sql', all_services_id=all_services_id)
    if result:
        return result[0]  # Возвращаем первый элемент списка
    return None


@blueprint_services.route('/', methods=['GET', 'POST'])
@group_required
def all_services():
    print('abba')
    if request.method == 'POST':
        page = int(request.form.get('page', 1))
    else:
        page = 1
    total_products = count_services()
    total_pages = -(-total_products // 10)
    services = get_all_from_db(page)
    print(services)
    return render_template("all_services.html", services=services, current_page=page, total_pages=total_pages)

@blueprint_services.route('/exit')
def exit_app():
    return render_template("main-menu.html")
