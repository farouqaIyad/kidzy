from db import db 
import datetime

class Review(db.Model):    
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    publish_date= db.Column(db.String(50))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    mother_name = db.Column(db.String(50))
    doctor = db.relationship('Doctor')

    def __init__(self, content, rating, doctor_id,mother_name):
        self.content = content
        self.rating = rating
        self.publish_date = datetime.date.today()
        self.doctor_id = doctor_id
        self.mother_name = mother_name

    @classmethod 
    def find_all_reviews(cls,doctor_id):
        return cls.query.filter_by(doctor_id = doctor_id).all()
    
    def json(self):
            return {"content":self.content, "rating":self.rating, "publish_date":self.publish_date,"review_writer_name":self.mother_name}
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()