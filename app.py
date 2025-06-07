from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Create the database on startup
with app.app_context():
    db.create_all()

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    vehicle = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='pending')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    taken = [(a.date, a.time) for a in appointments if a.status != 'cancelled']
    return jsonify(taken)

@app.route('/api/book', methods=['POST'])
def book_appointment():
    data = request.get_json()
    existing = Appointment.query.filter_by(date=data['date'], time=data['time']).first()
    if existing:
        return jsonify({'success': False, 'message': 'Time slot already booked.'}), 409

    new_appointment = Appointment(
        name=data['name'],
        phone=data['phone'],
        vehicle=data['vehicle'],
        date=data['date'],
        time=data['time']
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Appointment booked successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
