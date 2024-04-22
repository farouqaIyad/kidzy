from itertools import count
from db import db 
from model.profession import Professions
from model.reviews import Review

class Doctor(db.Model):
    __tablename__ = 'doctors'

    doctor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    gender = db.Column(db.Boolean)
    profession = db.Column(db.String(60))
    country = db.Column(db.String(50))
    city = db.Column(db.String(50))
    address = db.Column(db.String(50))
    contact_number = db.Column(db.String(12))
    open_time = db.Column(db.String(50))
    close_time = db.Column(db.String(50))

    def json(self):
        profession = Professions.find_by_id(self.profession)
        reviews = Review.find_all_reviews(self.doctor_id)
        sum_of_ratings = 0
        average_rating = 0
        counter = 0 
        for review in reviews:
            sum_of_ratings = sum_of_ratings + review.rating
            counter = counter +1
        if counter == 0:
            average_rating = 0
        else:
            average_rating = sum_of_ratings / counter
        return {
            "id":self.doctor_id,
            "Name":self.first_name +" "+ self.last_name,
            "Profession":profession.value,
            "address":self.country+" "+self.city+" "+self.address,
            "gender":self.gender,
            "rate":average_rating
        }
    
    def show_all(self):
        profession = Professions.find_by_id(self.profession)
        return {
        "id":self.doctor_id,
        "firstname":self.first_name,
        "lastname":self.last_name,
        "profession":profession.value,
        "Address":self.country+" - "+self.city+" - "+self.address,
        "contact":self.contact_number,
        "opentime":self.open_time,
        "closed_time":self.close_time,
        }
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(doctor_id = id).first()
