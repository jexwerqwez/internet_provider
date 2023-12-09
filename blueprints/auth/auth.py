import os
from typing import Optional, Dict
from flask import Blueprint, request, render_template, current_app, session, redirect, url_for
from sqlalchemy import text
from database.connect import engine

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')
current_dir = os.path.dirname(os.path.abspath(__file__))

def execute_query_from_file(filename, **params):
    with open(os.path.join(current_dir, 'sql', filename), 'r') as file:
        query = file.read().strip()
    with engine.connect() as connection:
        statement = text(query).bindparams(**params)
        result = connection.execute(statement)
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]

def define_user(login, password):
    external_user = execute_query_from_file('external_user.sql', login=login, password=password)
    internal_user = execute_query_from_file('internal_user.sql', login=login, password=password)
    if external_user:
        print(external_user[0])
        return external_user[0]
    elif internal_user:
        print(internal_user[0])
        return internal_user[0]
    else:
        print("User not found")
        return None

@auth.route('/', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
            user_info = define_user(login, password)
            if user_info:
                session['user_id'] = user_info['id']
                session['user_group'] = user_info.get('user_group')
                session.permanent = True
                return redirect(url_for('menu_choice'))
            else:
                return render_template('login.html', message='Пользователь не найден')
    return render_template('login.html', message='Повторите ввод')
