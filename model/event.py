from db import db 
from datetime import datetime

class eventModel(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer,primary_key = True)
    type = db.Column(db.Integer)
    details = db.Column(db.String(1000))
    day = db.Column(db.DateTime)
    baby_id = db.Column(db.Integer,db.ForeignKey('child.id'))

    def __init__(self, child_id, type, details, day):
        self.type = type
        self.details = details
        self.day = datetime.strptime(day,'%Y-%m-%d %H:%M')
        self.baby_id = child_id
    
    @classmethod
    def latest_events(cls,child_id):
        result = db.session.execute('select * from events where (type, day) in (select type, max(day)from events group by type) and events.baby_id = :val;',{'val':child_id}).all()
        return result
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f"{[self.id,self.type,self.details]}"
    
    @classmethod
    def find_by_child_id(cls, baby_id):
        result = db.session.execute('select * from events where events.baby_id = :val order by events.day desc;',{'val':baby_id}).all()
        return result  
      
    @classmethod
    def find_by_event_id(cls,event_id):
        return cls.query.filter_by(id = event_id).first()

    def json(self):
        return {
                "type":self.type,
                "details":self.details,
                "day":str(self.day.date()),
                "time":str(self.day.time())}
