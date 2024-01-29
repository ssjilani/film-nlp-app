from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Script(db.Model):
    __tablename__ = 'script_data'
    line_id = db.Column(db.String(500), primary_key=True)
    character_name = db.Column(db.String(100))
    dialogue = db.Column(db.String(5000))
    character_line_number = db.Column(db.Integer)
    film = db.Column(db.String(255))
    url = db.Column(db.String(500))
    franchise = db.Column(db.String(50))
