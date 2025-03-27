# Import the app instance
from app_factory import app, init_admin
from extensions import db
from models.quiz import Subject, Chapter, Quiz, Question, Option, Score
from models.admin import Admin

# Import all controllers to register routes
import controllers.auth_controller
import controllers.user_controller
import controllers.admin_controller
import controllers.quiz_controller

# Run the application
if __name__ == '__main__':
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables with new schema
        db.create_all()
        
        # Initialize admin account
        init_admin(app)
    app.run(debug=True)
