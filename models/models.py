from datetime import datetime

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    status = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to Chapter
    chapter = db.relationship('Chapter', backref='quizzes')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    chapters = db.relationship('Chapter', backref='subject', 
                             cascade='all, delete-orphan') 