from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models here so they are registered with SQLAlchemy
from models.user import User
from models.quiz import Subject, Chapter, Quiz, Question, Option, Score 