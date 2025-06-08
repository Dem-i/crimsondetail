from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)  # Replace with a static key in production

db = SQLAlchemy(app)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    vehicle = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='pending')

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/book', methods=['POST'])
def book_appointment():
    data = request.get_json()
    existing = Appointment.query.filter_by(date=data['date'], time=data['time']).first()
    if existing:
        return jsonify({'success': False, 'message': 'Time slot already booked.'}), 409

    new_appt = Appointment(
        name=data['name'],
        phone=data['phone'],
        vehicle=data['vehicle'],
        date=data['date'],
        time=data['time']
    )
    db.session.add(new_appt)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Appointment booked successfully!'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password123':  # 🔒 Change this in production!
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('login.html', error='Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    appointments = Appointment.query.all()
    return render_template('admin.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)
