
import os
from datetime import datetime, timezone
from flask import (Flask, render_template, request, redirect, url_for, flash)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError


# Initialize Flask
app = Flask(__name__)

app.config["SECRET_KEY"] = "replace-this-with-a-random-secret"

# Ensure the instance directory exists
os.makedirs(app.instance_path, exist_ok=True)


# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dendev.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Create User model
class User(db.Model):

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # User information
    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    # Store hashed password, never plain text
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # Account creation timestamp
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


@app.route('/register', methods=['GET', 'POST'])
def register():

    # If the user is visiting the page
    if request.method == 'GET':
        return render_template('register.html')

    # If the user submits the form
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    # 1. Validate empty fields
    if not username or not email or not password:
        flash('All fields are required.', 'danger')
        return redirect(url_for('register'))

    # 2. Validate field lengths
    if len(username) > 80 or len(email) > 120:
        flash('Username or email is too long.', 'danger')
        return redirect(url_for('register'))

    # 3. Basic email validation
    if '@' not in email or '.' not in email.split('@')[-1]:
        flash('Please enter a valid email address.', 'danger')
        return redirect(url_for('register'))

    # 4. Validate password length
    if len(password) < 8:
        flash('Password must contain at least 8 characters.', 'danger')
        return redirect(url_for('register'))

    # 5. Check whether username already exists
    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:
        flash('This username is already taken.', 'danger')
        return redirect(url_for('register'))

    # 6. Check whether email already exists
    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        flash('This email is already registered.', 'danger')
        return redirect(url_for('register'))

    # 7. Hash the password
    hashed_password = generate_password_hash(password)

    # 8. Create a new user object
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password
    )

    # 9. Save the user
    try:
        db.session.add(new_user)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        flash('Username or email is already in use.', 'danger')
        return redirect(url_for('register'))

    # 10. Registration successful
    flash('Your account has been created successfully!', 'success')

    return redirect(url_for('login'))

# Login page
@app.route('/')
def login():
    return render_template('login.html')


# Create database tables
with app.app_context():
    db.create_all()

# Run application
if __name__ == '__main__':
    app.run(debug=True)