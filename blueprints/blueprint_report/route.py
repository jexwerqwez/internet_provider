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
        try:
            result = connection.execute(text(query).bindparams(**params))
            connection.commit()  # Явный коммит изменений
            if result.returns_rows:
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
            else:
                return None
        except Exception as e:
            connection.rollback()  # Откат изменений в случае ошибки
            raise e  # Повторное возбуждение исключения для обработки в вызывающем коде



def report_exists(report_month, report_year):
    reports = execute_query_from_file('check_report_existence.sql', report_month=report_month, report_year=report_year)
    return len(reports) > 0


def get_all_reports():
    return execute_query_from_file('get_all_reports.sql')


def get_report_details_service(report_id):
    return execute_query_from_file('get_report_details_service.sql', report_id=report_id)


def get_report_details_balance(report_id):
    return execute_query_from_file('get_report_details_balance.sql', report_id=report_id)


def get_service_report(page, per_page=10):
    offset = (page - 1) * per_page
    return execute_query_from_file('view_service_report.sql', limit=per_page, offset=offset)


def show_all_service_reports():
    return execute_query_from_file('show_all_service_reports.sql')


def show_all_balance_reports():
    return execute_query_from_file('show_all_balance_reports.sql')



@blueprint_report.route('/', methods=['GET', 'POST'])
@group_required
def make_report():
    return render_template("report.html")


@blueprint_report.route('/create_report/<int:report_id>/<int:report_type>', methods=['GET', 'POST'])
@group_required
def create_report(report_id, report_type):
    if not group_validation(current_app.config['access_config'], 'blueprint_report.create_report'):
        return render_template('exceptions/admin_only.html')

    if request.method == 'POST':
        report_month = request.form.get('report_month')
        report_year = request.form.get('report_year')

        if report_exists(report_month, report_year):
            message = "Отчет за данный период уже существует."
            return render_template("create_report.html", report_id=report_id, report_type=report_type, message=message)

        if report_type == 1:
            execute_query_from_file('call_procedure_service_report.sql', report_month=report_month, report_year=report_year)
        elif report_type == 2:
            start_contract = request.form.get('start_contract_number')
            end_contract = request.form.get('end_contract_number')
            execute_query_from_file('call_procedure_balance_report.sql',
                                    start_num=start_contract,
                                    end_num=end_contract,
                                    report_month=report_month,
                                    report_year=report_year)

        return redirect(url_for("blueprint_report.view_report"))

    return render_template("create_report.html", report_id=report_id, report_type=report_type)


@blueprint_report.route('/view_report/<int:report_id>/<int:report_type>', methods=['GET'])
@group_required
def view_report(report_id, report_type):
    if report_type == 1:
        reports = show_all_service_reports()
    else:
        reports = show_all_balance_reports()
    print(reports)
    return render_template("view_report.html", reports=reports, report_id=report_id, report_type=report_type)

@blueprint_report.route('/view_report_details/<int:report_id>/<int:report_type>', methods=['GET'])
@group_required
def view_report_details(report_id, report_type):
    if report_type == 1:
        report_details = get_report_details_service(report_id)
    else:
        report_details = get_report_details_balance(report_id)
    print(report_type)
    return render_template("report_details.html", report_details=report_details, report_id=report_id, report_type=report_type)


@blueprint_report.route('/exit')
def exit_app():
    return render_template("main-menu.html")
