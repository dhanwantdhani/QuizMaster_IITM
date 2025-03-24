from app_factory import app, db
import models

# Create tables
with app.app_context():
    db.create_all()
    print("Database tables created!") 