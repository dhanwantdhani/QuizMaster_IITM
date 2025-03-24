from flask import render_template, request, redirect, url_for, flash, session
from app_factory import app, db
from controllers.decorators import admin_required
from models.quiz import Subject, Chapter, Quiz

# Admin login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        flash('Admin login successful!', 'success')
        session['user_type'], session['username'] = 'admin', username
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

# Admin dashboard
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Get all subjects with their associated chapters and quizzes
    subjects = Subject.query.all()
    return render_template('admin_dashboard.html', subjects=subjects)

# Admin stats
@app.route('/admin/stats')
@admin_required
def admin_stats(): return render_template('admin_stats.html')

# Admin summary
@app.route('/admin/summary')
@admin_required
def admin_summary(): return render_template('admin_summary.html')

# Add subject
@app.route('/admin/subject/add', methods=['GET'])
@admin_required
def add_subject_form():
    return render_template('add_subject.html')

@app.route('/admin/subject/add', methods=['POST'])
@admin_required
def add_subject():
    name = request.form.get('name')
    description = request.form.get('description')
    
    # Validate input
    if not name:
        flash('Subject name is required', 'error')
        return redirect(url_for('add_subject_form'))
    
    # Create new subject
    new_subject = Subject(name=name, description=description)
    db.session.add(new_subject)
    db.session.commit()
    
    flash('Subject added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Add chapter
@app.route('/admin/chapter/add', methods=['GET'])
@admin_required
def add_chapter_form():
    # Get all subjects for the dropdown
    subjects = Subject.query.all()
    return render_template('add_chapter.html', subjects=subjects)

@app.route('/admin/chapter/add', methods=['POST'])
@admin_required
def add_chapter():
    subject_id = request.form.get('subject_id')
    name = request.form.get('name')
    description = request.form.get('description')
    
    # Validate
    if not subject_id or not name:
        flash('Subject and chapter name are required', 'error')
        return redirect(url_for('add_chapter_form'))
    
    # Create new chapter
    new_chapter = Chapter(
        name=name,
        description=description,
        subject_id=subject_id
    )
    db.session.add(new_chapter)
    db.session.commit()
    
    flash('Chapter added successfully', 'success')
    return redirect(url_for('admin_dashboard')) 