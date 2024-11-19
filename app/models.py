from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    full_name = db.Column(db.String(150), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.Integer, nullable=True)  # 0, 1, 2
    street_address = db.Column(db.String(150), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    zip = db.Column(db.String(20), nullable=True)
    diagnose_date = db.Column(db.Date, nullable=True)
    blood_glucose_level = db.Column(db.Float, nullable=True)
    blood_glucose_fasting_level = db.Column(db.Float, nullable=True)
    medications = db.Column(db.String, nullable=True)
    medical_conditions = db.Column(db.String, nullable=True)
    dietary_pref = db.Column(db.Integer, nullable=True)  # 0, 1, 2, 3, 4, 5
    physical_activity = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    management_goals = db.Column(db.String, nullable=True)
    learning_preference = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Integer, default=1, nullable=False)

class LoginHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('login_history', lazy=True))
    
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)  # New field for chat titles
    last_message = db.Column(db.Text, nullable=True)   # New field for the last message
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(10))  # 'user' or 'assistant'
    content = db.Column(db.Text)  # Chat content
    user = db.relationship('User', backref=db.backref('chat_history', lazy=True))