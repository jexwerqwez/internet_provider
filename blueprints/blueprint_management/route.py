import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import text
from database.connect import engine
from access import group_required

blueprint_management = Blueprint('blueprint_management', __name__, template_folder='templates', static_folder='static')
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


def get_all_from_db(page, per_page=10):
    offset = (page - 1) * per_page
    return execute_query_from_file('get_all_services.sql', limit=per_page, offset=offset)


@blueprint_management.route('/', methods=['GET', 'POST'])
@group_required
def management():
    print('abba')
    if request.method == 'POST':
        page = int(request.form.get('page', 1))
    else:
        page = 1
    total_products = count_services()
    total_pages = -(-total_products // 10)
    services = get_all_from_db(page)
    print(services)
    return render_template("management.html", services=services, current_page=page, total_pages=total_pages)


@blueprint_management.route('/add_services', methods=['POST'])
@group_required
def add_service():
    name = request.form.get('name')
    cost = request.form.get('cost')
    description = request.form.get('description')
    type = request.form.get('type')

    insert_query = text("INSERT INTO all_services (name, cost, description, type) VALUES (:name, :cost, :description, :type)")

    try:
        with engine.connect() as connection:
            # Начинаем транзакцию вручную
            trans = connection.begin()
            try:
                connection.execute(insert_query, {'name': name, 'cost': cost, 'description': description, 'type': type})
                trans.commit()
                flash('Услуга успешно добавлена', 'success')
            except Exception as e:
                trans.rollback()
                flash(f'Ошибка при добавлении услуги: {e}', 'error')
                return render_template("error_message.html",
                                       message="Произошла ошибка при выполнении транзакции. Пожалуйста, попробуйте позже.")
    except Exception as e:
        flash(f'Ошибка при подключении к базе данных: {e}', 'error')
        return render_template("error_message.html",
                               message="Произошла ошибка при выполнении транзакции. Пожалуйста, попробуйте позже.")

    return redirect(url_for('blueprint_management.management'))



@blueprint_management.route('/exit')
def exit_app():
    return render_template("main-menu.html")
