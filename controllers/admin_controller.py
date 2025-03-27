from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app_factory import app, db
from controllers.decorators import admin_required
from models.quiz import Subject, Chapter, Quiz, Question, Option, Score
# Remove duplicate import lines to avoid conflicts
# from models import Subject
# from models import db
from datetime import datetime
from models.admin import Admin

# Admin login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # Clear any existing flash messages when displaying the login page
    if request.method == 'GET':
        session.pop('_flashes', None)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username='admin').first()
        
        if not admin or not admin.check_password(password):
            flash('Invalid username or password', 'error')
            return render_template('admin_login.html')
        
        # If credentials are correct
        session['user_type'] = 'admin'
        session['username'] = username
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
    # Clear any existing flash messages when displaying the form
    session.pop('_flashes', None)
    return render_template('add_subject.html')

@app.route('/admin/subject/add', methods=['POST'])
@admin_required
def add_subject():
    try:
        name = request.form.get('name')
        
        if not name:
            flash('Subject name is required', 'error')
            return redirect(url_for('add_subject_form'))
        
        new_subject = Subject(
            name=name
        )
        
        db.session.add(new_subject)
        db.session.commit()
        
        flash('Subject added successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding subject: {str(e)}', 'error')
        return redirect(url_for('add_subject_form'))

# Add chapter
@app.route('/admin/subject/<int:subject_id>/add-chapter', methods=['GET'])
@admin_required
def add_chapter_form(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    return render_template('add_chapter.html', subject=subject)

@app.route('/admin/subject/<int:subject_id>/add-chapter', methods=['POST'])
@admin_required
def add_chapter(subject_id):
    try:
        name = request.form.get('name')
        
        if not name:
            flash('Chapter name is required', 'error')
            return redirect(url_for('add_chapter_form', subject_id=subject_id))
        
        new_chapter = Chapter(
            name=name,
            subject_id=subject_id
        )
        
        db.session.add(new_chapter)
        db.session.commit()
        
        flash('Chapter added successfully', 'success')
        return redirect(url_for('chapter_settings', subject_id=subject_id))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding chapter: {str(e)}', 'error')
        return redirect(url_for('add_chapter_form', subject_id=subject_id))

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
        
        # First, get all chapters for this subject
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        
        # For each chapter, delete associated quizzes and their questions/options
        for chapter in chapters:
            # Get all quizzes for this chapter
            quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
            
            for quiz in quizzes:
                # Delete all questions and their options for this quiz
                questions = Question.query.filter_by(quiz_id=quiz.id).all()
                for question in questions:
                    # Delete options for this question
                    Option.query.filter_by(question_id=question.id).delete()
                    # Delete the question
                    db.session.delete(question)
                
                # Delete scores associated with this quiz
                Score.query.filter_by(quiz_id=quiz.id).delete()
                
                # Delete the quiz
                db.session.delete(quiz)
            
            # Delete the chapter
            db.session.delete(chapter)
        
        # Finally, delete the subject
        db.session.delete(subject)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting subject: {str(e)}")  # Add logging
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('user_login'))

# Add these routes for editing subjects
@app.route('/admin/subject/<int:subject_id>/edit', methods=['GET'])
@admin_required
def edit_subject_form(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    return render_template('edit_subject.html', subject=subject)

@app.route('/admin/subject/<int:subject_id>/edit', methods=['POST'])
@admin_required
def edit_subject(subject_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        name = request.form.get('name')
        
        if not name:
            flash('Subject name is required', 'error')
            return redirect(url_for('edit_subject_form', subject_id=subject_id))
        
        # Update the subject name
        subject.name = name
        db.session.commit()
        
        flash('Subject updated successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating subject: {str(e)}', 'error')
        return redirect(url_for('edit_subject_form', subject_id=subject_id))

@app.route('/admin/chapter/<int:chapter_id>/add-quiz', methods=['GET'])
@admin_required
def add_quiz_form(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    return render_template('add_quiz.html', chapter=chapter)

@app.route('/admin/chapter/<int:chapter_id>/add-quiz', methods=['POST'])
@admin_required
def add_quiz_to_chapter(chapter_id):
    try:
        chapter = Chapter.query.get_or_404(chapter_id)
        
        # Get quiz details from form
        title = request.form.get('title')
        description = request.form.get('description', '')
        duration = request.form.get('duration')
        
        if not title or not duration:
            flash('Quiz title and duration are required', 'error')
            return redirect(url_for('add_quiz_form', chapter_id=chapter_id))
        
        # Create new quiz
        new_quiz = Quiz(
            title=title,
            description=description,
            duration=int(duration),
            chapter_id=chapter_id,
            status='draft',
            date=datetime.now()
        )
        
        db.session.add(new_quiz)
        db.session.commit()
        
        flash('Quiz added successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding quiz: {str(e)}', 'error')
        return redirect(url_for('add_quiz_form', chapter_id=chapter_id))

@app.route('/admin/quiz/create', methods=['GET'])
@admin_required
def create_quiz_form():
    subjects = Subject.query.all()
    return render_template('add_quiz.html', subjects=subjects)

@app.route('/api/subjects/<int:subject_id>/chapters')
@admin_required
def get_subject_chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = [{'id': chapter.id, 'name': chapter.name} for chapter in subject.chapters]
    return jsonify(chapters)

@app.route('/admin/quiz/create', methods=['POST'])
@admin_required
def create_quiz():
    try:
        data = request.get_json()
        chapter_id = data.get('chapter_id')
        name = data.get('title')
        quiz_date = data.get('quiz_date')
        quiz_time = data.get('quiz_time')
        duration = data.get('duration')

        if not all([chapter_id, name, quiz_date, quiz_time, duration]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400

        # Parse the date and time
        quiz_datetime = datetime.strptime(f"{quiz_date} {quiz_time}", "%Y-%m-%d %H:%M")
        
        # Convert duration from HH:MM to minutes
        duration_parts = duration.split(':')
        duration_minutes = int(duration_parts[0]) * 60 + int(duration_parts[1])

        new_quiz = Quiz(
            name=name,
            chapter_id=chapter_id,
            quiz_date=quiz_datetime,
            duration=duration_minutes,
            created_at=datetime.utcnow()
        )

        db.session.add(new_quiz)
        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        print(f"Error creating quiz: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/quiz/<int:quiz_id>/edit', methods=['GET'])
@admin_required
def edit_quiz_form(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    subjects = Subject.query.all()
    return render_template('edit_quiz.html', quiz=quiz, subjects=subjects)

@app.route('/admin/quiz/<int:quiz_id>/edit', methods=['POST'])
@admin_required
def edit_quiz(quiz_id):
    try:
        data = request.get_json()
        quiz = Quiz.query.get_or_404(quiz_id)
        
        chapter_id = data.get('chapter_id')
        name = data.get('title')  # We'll use this as the name

        if not all([chapter_id, name]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400

        # Update quiz
        quiz.name = name
        quiz.chapter_id = chapter_id
        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/quiz/<int:quiz_id>/delete', methods=['DELETE'])
@admin_required
def delete_quiz(quiz_id):
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        db.session.delete(quiz)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/admin/quiz/<int:quiz_id>/manage')
@admin_required
def manage_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('manage_quiz.html', quiz=quiz)

@app.route('/admin/quiz/<int:quiz_id>/question/add', methods=['GET'])
@admin_required
def admin_add_question_form(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('add_question.html', quiz=quiz)

@app.route('/admin/quiz/<int:quiz_id>/question/add', methods=['POST'])
@admin_required
def admin_add_question(quiz_id):
    try:
        data = request.get_json()
        question_text = data.get('question_text')
        options = data.get('options', [])

        if not question_text or not options:
            return jsonify({'success': False, 'message': 'Question and options are required'}), 400

        # Create new question
        new_question = Question(
            text=question_text,
            quiz_id=quiz_id
        )
        db.session.add(new_question)
        db.session.flush()  # To get the question ID

        # Add options
        for option_data in options:
            option = Option(
                text=option_data['text'],
                is_correct=option_data['is_correct'],
                question_id=new_question.id
            )
            db.session.add(option)

        db.session.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        print(f"Error adding question: {str(e)}")  # Add logging
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/question/<int:question_id>/delete', methods=['DELETE'])
@admin_required
def delete_question(question_id):
    try:
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/admin/quiz/<int:quiz_id>/question/<int:question_id>/edit', methods=['GET'])
@admin_required
def edit_question_form(quiz_id, question_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    question = Question.query.get_or_404(question_id)
    return render_template('edit_question.html', quiz=quiz, question=question)

@app.route('/admin/quiz/<int:quiz_id>/question/<int:question_id>/edit', methods=['POST'])
@admin_required
def edit_question(quiz_id, question_id):
    try:
        data = request.get_json()
        question = Question.query.get_or_404(question_id)
        
        question_text = data.get('question_text')
        options = data.get('options', [])

        if not question_text or not options:
            return jsonify({'success': False, 'message': 'Question and options are required'}), 400

        # Update question
        question.text = question_text
        
        # Delete existing options
        Option.query.filter_by(question_id=question.id).delete()
        
        # Add new options
        for option_data in options:
            option = Option(
                text=option_data['text'],
                is_correct=option_data['is_correct'],
                question_id=question.id
            )
            db.session.add(option)

        db.session.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/quiz/<int:quiz_id>/question/<int:question_id>/delete', methods=['DELETE'])
@admin_required
def admin_delete_quiz_question(quiz_id, question_id):
    try:
        # First delete all options associated with the question
        question = Question.query.get_or_404(question_id)
        Option.query.filter_by(question_id=question.id).delete()
        
        # Then delete the question
        db.session.delete(question)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/subject-settings')
@admin_required
def subject_settings():
    subjects = Subject.query.all()
    return render_template('subject_settings.html', subjects=subjects)

@app.route('/admin/subject/<int:subject_id>/chapter-settings')
@admin_required
def chapter_settings(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    return render_template('chapter_settings.html', subject=subject)

@app.route('/admin/subject/<int:subject_id>/chapter/<int:chapter_id>/edit', methods=['GET'])
@admin_required
def edit_chapter(subject_id, chapter_id):
    subject = Subject.query.get_or_404(subject_id)
    chapter = Chapter.query.get_or_404(chapter_id)
    return render_template('edit_chapter.html', subject=subject, chapter=chapter)

@app.route('/admin/subject/<int:subject_id>/chapter/<int:chapter_id>/edit', methods=['POST'])
@admin_required
def update_chapter(subject_id, chapter_id):
    try:
        chapter = Chapter.query.get_or_404(chapter_id)
        name = request.form.get('name')
        
        if not name:
            flash('Chapter name is required', 'error')
            return redirect(url_for('edit_chapter', subject_id=subject_id, chapter_id=chapter_id))
        
        chapter.name = name
        db.session.commit()
        
        flash('Chapter updated successfully', 'success')
        return redirect(url_for('chapter_settings', subject_id=subject_id))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating chapter: {str(e)}', 'error')
        return redirect(url_for('edit_chapter', subject_id=subject_id, chapter_id=chapter_id))

@app.route('/admin/chapter/<int:chapter_id>/delete', methods=['DELETE'])
@admin_required
def delete_chapter(chapter_id):
    try:
        chapter = Chapter.query.get_or_404(chapter_id)
        
        # Delete associated quizzes first
        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        for quiz in quizzes:
            # Delete questions and options for each quiz
            questions = Question.query.filter_by(quiz_id=quiz.id).all()
            for question in questions:
                Option.query.filter_by(question_id=question.id).delete()
                db.session.delete(question)
            db.session.delete(quiz)
            
        db.session.delete(chapter)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400 