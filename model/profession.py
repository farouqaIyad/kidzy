from db import db 

class Professions(db.Model):
    __tablename__ = 'professions'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(50))

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id = id).first()