from flask import render_template, request, redirect, url_for, flash
from app_factory import app
from controllers.decorators import user_required, admin_required
from models.quiz import Quiz, Question, Option
from app_factory import db

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
@app.route('/admin/question/add/<int:quiz_id>', methods=['GET'])
@admin_required
def add_question_form(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('add_question.html', quiz=quiz)

@app.route('/admin/question/add/<int:quiz_id>', methods=['POST'])
@admin_required
def add_question(quiz_id):
    title = request.form.get('title')
    statement = request.form.get('statement')
    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    option3 = request.form.get('option3')
    option4 = request.form.get('option4')
    correct_option = request.form.get('correct_option')
    
    # Validate
    if not all([title, statement, option1, option2, correct_option]):
        flash('Required fields missing', 'error')
        return redirect(url_for('add_question_form', quiz_id=quiz_id))
    
    # Create question
    new_question = Question(
        text=statement,
        quiz_id=quiz_id
    )
    db.session.add(new_question)
    db.session.flush()  # Get question ID before committing
    
    # Add options
    options = [option1, option2, option3, option4]
    for i, option_text in enumerate(options, 1):
        if option_text:
            is_correct = (str(i) == correct_option)
            option = Option(
                text=option_text,
                is_correct=is_correct,
                question_id=new_question.id
            )
            db.session.add(option)
    
    db.session.commit()
    flash('Question added successfully', 'success')
    return redirect(url_for('view_quiz', quiz_id=quiz_id)) 