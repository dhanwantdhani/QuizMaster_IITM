from functools import wraps
from flask import redirect, url_for, flash, session

# Authentication decorators
def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'user':
            flash('Please login first!', 'error')
            return redirect(url_for('user_login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'admin':
            flash('Please login as admin first!', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated 