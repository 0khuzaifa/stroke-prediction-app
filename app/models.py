from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, unique=True, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Float, nullable=False)
    hypertension = db.Column(db.Integer, nullable=False)
    ever_married = db.Column(db.String(10), nullable=False)
    work_type = db.Column(db.String(50), nullable=False)
    residence_type = db.Column(db.String(50), nullable=False)
    avg_glucose_level = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=True)
    smoking_status = db.Column(db.String(50), nullable=False)
    stroke = db.Column(db.Integer, nullable=False)
