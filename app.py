# Import the app instance
from app_factory import app

# Import all controllers to register routes
import controllers.auth_controller
import controllers.user_controller
import controllers.admin_controller
import controllers.quiz_controller

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
