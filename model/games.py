from db import db 


class GamesModel(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key = True)
    game_number = db.Column(db.Integer)
    Date = db.Column(db.String(50))
    begin_time = db.Column(db.String(30))
    duration = db.Column(db.String(30))
    success = db.Column(db.Boolean)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))

    def __init__(self, success,game_number, Date,begin_time, duration, child_id):
        self.success = success
        self.game_number = game_number
        self.Date = Date
        self.begin_time = begin_time
        self.duration = duration
        self.child_id = child_id

    @classmethod
    def find(cls,game_number, child_id):
        return cls.query.filter_by(game_number = game_number, child_id = child_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return{
            "name":self.game_number,
            "date":self.Date,
            "begin_time":self.begin_time,
            "duration":self.duration,
            "success":self.success
        }