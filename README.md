# Quiz Master

A simple quiz application with user authentication and role-based access.

## Features

- Role selection (Admin or User)
- Admin login
- User login and registration
- Basic session management
- Role-specific dashboards

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure the virtual environment is activated
2. Run the Flask application:
   ```
   python app.py
   ```
3. Open your browser and navigate to `http://127.0.0.1:5000/`

## Project Structure

- `app.py`: Main Flask application
- `templates/`: Jinja2 templates
  - `base.html`: Base template with common structure
  - `index.html`: Landing page with role selection
  - `user_choice.html`: User options page (login or register)
  - `user_login.html`: User login page
  - `admin_login.html`: Admin login page
  - `register.html`: User registration page
- `static/`: Static files
  - `css/`: CSS stylesheets
    - `style.css`: Main stylesheet
