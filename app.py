from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



import os

app = Flask(__name__)
app.secret_key = 'Wqv8#KzN3@eP$Y6m2^XR9cBL!fdA*1uQztGV4s0J'  # Replace with a secure key in production
import os  # make sure this is at the top with your other imports

app = Flask(__name__)
app.secret_key = 'Wqv8#KzN3@eP$Y6m2^XR9cBL!fdA*1uQztGV4s0J'  # or use os.environ.get(...) if you prefer

if os.environ.get('RENDER'):
    db_path = '/tmp/appointments.db'  # writable location on Render
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'appointments.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']
    service = request.form['service']
    appointment = Appointment(name=name, date=date, time=time, service=service)
    db.session.add(appointment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if 'logged_in' in session:
        appointments = Appointment.query.all()
        return render_template('admin.html', appointments=appointments)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple login logic (replace with secure method)
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
