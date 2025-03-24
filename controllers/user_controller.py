from flask import render_template, request, redirect, url_for, flash, session
from app_factory import app, db
from models.user import User
from controllers.decorators import user_required
from datetime import datetime

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
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user in database
        user = User.query.filter_by(username=username, is_admin=False).first()
        
        if user and user.check_password(password):
            session['user_type'] = 'user'
            session['username'] = username
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('user_login.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        qualification = request.form.get('qualification')
        dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d').date()
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html')
        
        # Create new user
        new_user = User(
            username=username,
            fullname=fullname,
            qualification=qualification,
            dob=dob,
            is_admin=False
        )
        new_user.set_password(password)
        
        # Add and commit to database
        db.session.add(new_user)
        db.session.commit()
        
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