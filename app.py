
from flask import Flask, render_template

# Initialize Flask application
app = Flask(__name__)


# Login page
@app.route('/')
def login():
    return render_template('login.html')


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
