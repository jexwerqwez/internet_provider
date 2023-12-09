from functools import wraps

from flask import session, render_template, current_app, request, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('auth.start_auth'))
    print('aboba')
    return wrapper


def group_validation(config: dict, endpoint: str = None) -> bool:
    endpoint_app = endpoint if endpoint else request.endpoint.split('.')[0]
    print('Endpoint app is:', endpoint_app)
    if 'user_group' in session:
        user_group = session['user_group']
        print('USER GROUP IS', user_group)
        if user_group is None and 'typical' in config and endpoint_app in config['typical']:
            return True
        print('Config for user group:', config.get(user_group))
        if user_group in config and endpoint_app in config[user_group]:
            return True
    return False



def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            print("Group validation passed")
            return f(*args, **kwargs)
        print("Group validation failed")
        return render_template('exceptions/internal_only.html')
    return wrapper
