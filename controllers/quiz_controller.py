from flask import render_template, request, redirect, url_for, flash
from app_factory import app
from controllers.decorators import user_required, admin_required

# View quiz details
@app.route('/quiz/view/<int:quiz_id>')
@user_required
def view_quiz(quiz_id): return render_template('view_quiz.html', quiz_id=quiz_id)

# Take quiz
@app.route('/quiz/take/<int:quiz_id>')
@user_required
def take_quiz(quiz_id): return render_template('take_quiz.html', quiz_id=quiz_id)

# Add quiz
@app.route('/admin/quiz/add', methods=['POST'])
@admin_required
def add_quiz():
    # Process data...
    flash('Quiz added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Add question
@app.route('/admin/question/add', methods=['POST'])
@admin_required
def add_question():
    # Process data...
    flash('Question added successfully', 'success')
    return redirect(url_for('admin_dashboard')) 