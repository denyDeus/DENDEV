
import os

from datetime import datetime, timezone

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# Initialize Flask
app = Flask(__name__)


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