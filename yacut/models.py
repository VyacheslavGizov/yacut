from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)  # обязательное
    short = db.Column(db.String(16), unique=True, nullable=False)  # обязательное
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
