from sqlalchemy.sql import func
from main.db import db


class PlateModel(db.Model):
    __tablename__ = 'plates'

    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(8), nullable=False)
    timestamp = db.Column(
        'timestamp',
        db.TIMESTAMP,
        server_default=func.now(),
        nullable=False)

    def __init__(self, plate):
        self.plate = plate

    def json(self):
        return {'plate': self.plate,
                'timestamp': self.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')}

    @classmethod
    def find_by_value(cls, value):
        return cls.query.filter_by(plate=value).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
