from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app_factory import app, db
from controllers.decorators import admin_required
from models.quiz import Subject, Chapter, Quiz
from models import Subject
from models import db  # or you could import from your app.py if db is defined there

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
    subjects = Subject.query.all()
    # Get all quizzes without filtering by type since we don't have that field
    quizzes = Quiz.query.all()
    return render_template('admin_dashboard.html', 
                         subjects=subjects,
                         quizzes=quizzes)

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
    try:
        data = request.json
        new_subject = Subject(
            name=data['name'],
            description=data.get('description', '')  # Optional description
        )
        db.session.add(new_subject)
        db.session.commit()
        return jsonify({'success': True, 'id': new_subject.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

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

@app.route('/admin/subject/<int:subject_id>')
@admin_required
def view_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    return render_template('view_subject.html', subject=subject)

@app.route('/admin/subject/<int:subject_id>/delete', methods=['DELETE'])
@admin_required
def delete_subject(subject_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('user_login')) 