import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from sqlalchemy import text, exc
from database.connect import engine
from access import group_required, group_validation

blueprint_report = Blueprint('blueprint_report', __name__, template_folder='templates', static_folder='static')
current_dir = os.path.dirname(os.path.abspath(__file__))

def execute_query_from_file(filename, **params):
    with open(os.path.join(current_dir, 'sql', filename), 'r') as file:
        query = file.read().strip()
    with engine.connect() as connection:
        result = connection.execute(text(query).bindparams(**params))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]

def get_categories():
    with open(os.path.join(current_dir, 'sql/get_category_img.sql'), 'r') as file:
        query = file.read().strip()
    with engine.connect() as connection:
        result = connection.execute(text(query))

        return [{'name': row[0], 'image': row[1]} for row in result]


def get_prod_name():
    with open(os.path.join(current_dir, 'sql/get_prod_name.sql'), 'r') as file:
        query = file.read().strip()
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return [{'id': row[0], 'name': row[1]} for row in result]


def count_products():
    with open(os.path.join(current_dir, 'sql/count_products.sql'), 'r') as file:
        query = file.read().strip()
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchone()[0]

def get_all_from_db(page, per_page=10):
    offset = (page - 1) * per_page
    return execute_query_from_file('get_all_services.sql', limit=per_page, offset=offset)


def get_report_data(report_id):
    table_map = {1: 'report_revenue', 2: 'report_turnover', 3: 'report_producttop'}
    table_name = table_map.get(report_id)
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT * FROM {table_name}"))
        columns = result.keys()
        report_data = [dict(zip(columns, row)) for row in result.fetchall()]
        return report_data


def process_report_creation(report_id, date_from, date_to, report_data):
    table_map = {1: 'report_revenue', 2: 'report_turnover', 3: 'report_producttop'}
    table_name = table_map.get(report_id)

    with engine.connect() as connection:
        query = text(
            f"INSERT INTO {table_name} (date_from, date_to, report_data) VALUES (:date_from, :date_to, :report_data)"
        )
        connection.execute(query, {"date_from": date_from, "date_to": date_to, "report_data": report_data})
        connection.commit()


@blueprint_report.route('/', methods=['GET', 'POST'])
@group_required
def make_report():
    return render_template("report.html")


@blueprint_report.route('/create_report/<int:report_id>', methods=['GET', 'POST'])
@group_required
def create_report(report_id):
    if not group_validation(current_app.config['access_config'], 'blueprint_report.create_report'):
        return render_template('exceptions/admin_only.html')
    if request.method == 'POST':
        date_from = request.form['date_from']
        date_to = request.form['date_to']
        report_data = request.form.get('prod_name') if report_id == 1 else request.form.get('prod_category', 'aboba')
        process_report_creation(report_id, date_from, date_to, report_data)
        return redirect(url_for("blueprint_report.make_report"))

    categories = get_categories()
    products = get_prod_name()
    return render_template("create_report.html", categories=categories, products=products, report_id=report_id)


@blueprint_report.route('/view_report/<int:report_id>', methods=['GET', 'POST'])
@group_required
def view_report(report_id):
    if not group_validation(current_app.config['access_config'], 'blueprint_report.view_report'):
        return render_template('exceptions/manager_only.html')
    report_data = get_report_data(report_id)
    return render_template("view_report.html", report_data=report_data, report_id=report_id)


@blueprint_report.route('/exit')
def exit_app():
    return render_template("main-menu.html")
