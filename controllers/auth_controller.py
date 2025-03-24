from flask import redirect, url_for, flash, session
from app_factory import app

# Import decorators from decorators.py - no circular reference
from controllers.decorators import user_required, admin_required

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index')) 