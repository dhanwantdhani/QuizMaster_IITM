from flask import Flask
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    return app

app = create_app()

def init_admin(app):
    from models.admin import Admin
    
    with app.app_context():
        # Check if admin already exists
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            # Create admin account with default credentials
            admin = Admin(username='admin')
            admin.set_password('admin123')  # Set a strong default password
            db.session.add(admin)
            db.session.commit() 