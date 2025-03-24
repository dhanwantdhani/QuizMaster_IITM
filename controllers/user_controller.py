from flask import render_template, request, redirect, url_for, flash, session
from app_factory import app
from controllers.decorators import user_required

# Main landing page
@app.route('/')
def index(): return render_template('index.html')

# User choice page (login or register)
@app.route('/user')
def user_choice(): return render_template('user_choice.html')

# User login
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        flash('Login successful!', 'success')
        session['user_type'], session['username'] = 'user', username
        return redirect(url_for('dashboard'))
    return render_template('user_login.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Registration logic here
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('user_login'))
    return render_template('register.html')

# User dashboard
@app.route('/dashboard')
@user_required
def dashboard(): return render_template('user_dashboard.html')

# User scores
@app.route('/scores')
@user_required
def scores(): return render_template('scores.html')

# User summary
@app.route('/summary')
@user_required
def summary(): return render_template('summary.html') 