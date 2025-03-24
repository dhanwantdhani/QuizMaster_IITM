from flask import render_template, request, redirect, url_for, flash, session
from app_factory import app
from controllers.decorators import admin_required

# Admin login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        flash('Admin login successful!', 'success')
        session['user_type'], session['username'] = 'admin', username
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

# Admin dashboard
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard(): return render_template('admin_dashboard.html')

# Admin stats
@app.route('/admin/stats')
@admin_required
def admin_stats(): return render_template('admin_stats.html')

# Admin summary
@app.route('/admin/summary')
@admin_required
def admin_summary(): return render_template('admin_summary.html')

# Add subject
@app.route('/admin/subject/add', methods=['POST'])
@admin_required
def add_subject():
    # Process data...
    flash('Subject added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# Add chapter
@app.route('/admin/chapter/add', methods=['POST'])
@admin_required
def add_chapter():
    # Process data...
    flash('Chapter added successfully', 'success')
    return redirect(url_for('admin_dashboard')) 