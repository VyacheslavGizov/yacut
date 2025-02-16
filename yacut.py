from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from settings import Config


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)  # обязательное
    short = db.Column(db.String(16), unique=True, nullable=False)  # обязательное
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index_view():
    db.create_all()
    url = URLMap(
        original='dfkfhdkjhdfkfj',
        short='dfkjhfd'
    )
    db.session.add(url)
    db.session.commit()
    return 'Совсем скоро тут будет случайное мнение о фильме!'


if __name__ == '__main__':
    app.run()
