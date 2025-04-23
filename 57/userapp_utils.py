from functools import wraps
from flask import session, redirect, url_for, request, jsonify

def login_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication error'}), 401
        return f(*args, **kwargs)
    return decorated_function

def login_required_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('userapp.login_view', next=request.url))
        return f(*args, **kwargs)
    return decorated_function