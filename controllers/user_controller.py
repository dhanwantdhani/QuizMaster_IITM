from flask import render_template, request, redirect, url_for, flash, session
from app_factory import app, db
from models.user import User
from models.quiz import Subject, Chapter, Quiz, Score
from controllers.decorators import user_required
from datetime import datetime
from werkzeug.security import generate_password_hash

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
def dashboard():
    user = User.query.get(session['user_id'])
    subjects = Subject.query.all()
    return render_template('user_dashboard.html', user=user, subjects=subjects)

# User profile
@app.route('/profile')
@user_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

# Edit profile
@app.route('/profile/edit', methods=['GET', 'POST'])
@user_required
def edit_profile():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.fullname = request.form.get('fullname')
        user.qualification = request.form.get('qualification')
        user.dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d').date()
        
        # Handle password change if provided
        new_password = request.form.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html', user=user)

# User summary
@app.route('/summary')
@user_required
def summary():
    user = User.query.get(session['user_id'])
    scores = Score.query.filter_by(user_id=user.id).order_by(Score.created_at.desc()).all()
    subjects = Subject.query.all()
    return render_template('summary.html', user=user, scores=scores, subjects=subjects)

# User scores
@app.route('/scores')
@user_required
def scores():
    user = User.query.get(session['user_id'])
    scores = Score.query.filter_by(user_id=user.id).order_by(Score.created_at.desc()).all()
    return render_template('scores.html', user=user, scores=scores)

# View chapter and its quizzes
@app.route('/chapter/<int:chapter_id>')
@user_required
def view_chapter(chapter_id):
    user = User.query.get(session['user_id'])
    chapter = Chapter.query.get_or_404(chapter_id)
    return render_template('view_chapter.html', chapter=chapter, user=user) 