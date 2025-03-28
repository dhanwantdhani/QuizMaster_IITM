from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app_factory import app
from controllers.decorators import user_required, admin_required
from models.quiz import Quiz, Question, Option, Score
from models.user import User
from app_factory import db
from datetime import datetime

# View available quizzes
@app.route('/quizzes')
@user_required
def list_quizzes():
    quizzes = Quiz.query.all()
    return render_template('list_quizzes.html', quizzes=quizzes)

# View quiz details
@app.route('/quiz/view/<int:quiz_id>')
@user_required
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('view_quiz.html', quiz=quiz)

# Take quiz
@app.route('/quiz/take/<int:quiz_id>', methods=['GET', 'POST'])
@user_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        # Get user's answers
        answers = {}
        completion_time = request.form.get('completion_time', 0)  # Time taken in seconds
        
        for question in quiz.questions:
            answer_id = request.form.get(f'question_{question.id}')
            if answer_id:
                answers[question.id] = int(answer_id)
        
        # Calculate score
        correct_answers = 0
        total_questions = len(quiz.questions)
        
        for question_id, answer_id in answers.items():
            question = Question.query.get(question_id)
            correct_option = Option.query.filter_by(question_id=question_id, is_correct=True).first()
            if correct_option and correct_option.id == answer_id:
                correct_answers += 1
        
        # Calculate percentage
        score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Save score
        score = Score(
            user_id=session['user_id'],
            quiz_id=quiz_id,
            score=score_percentage,
            max_score=100,
            completion_time=completion_time,
            created_at=datetime.utcnow()
        )
        db.session.add(score)
        db.session.commit()
        
        flash(f'Quiz completed! Your score: {score_percentage:.1f}%', 'success')
        return redirect(url_for('view_scores'))
    
    return render_template('take_quiz.html', quiz=quiz)

# View scores
@app.route('/scores')
@user_required
def view_scores():
    scores = Score.query.filter_by(user_id=session['user_id']).order_by(Score.created_at.desc()).all()
    return render_template('scores.html', scores=scores)

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