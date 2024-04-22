from db import db 
from builtfunction import get_status
from datetime import datetime,date

class ChildModel(db.Model):
    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(45))
    date_of_birth = db.Column(db.Date)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    gender = db.Column(db.Integer)
    mother_id = db.Column(db.Integer, db.ForeignKey('Mother.id'))
    events = db.relationship('eventModel',backref = 'child')

    def __init__(self, name, height, weight,
     gender, mother_id,date_of_birth):
        self.name = name 
        self.date_of_birth = datetime.strptime(date_of_birth,'%Y-%m-%d').date()
        self.height = height
        self.weight = weight
        self.gender = gender
        self.mother_id = mother_id
    
    def json(self):
        return {"name":self.name,"gender":self.gender,"date_of_birth":str(self.date_of_birth),"height":self.height,"weight":self.weight}
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_all(cls,mother_id):
        return cls.query.filter_by(mother_id = mother_id).all()
    
    @classmethod
    def find_child(cls, child_id):
        return cls.query.filter_by(id = child_id).first()


class averageChild(db.Model):
    __tablename__ = 'weight distribution'

    gender = db.Column(db.Integer, primary_key= True)
    age = db.Column(db.Integer, primary_key = True)
    lowest_weight = db.Column(db.Float)
    highest_weight = db.Column(db.Float)
    lowest_height = db.Column(db.Float)
    highest_height = db.Column(db.Float)

    @classmethod
    def find_data(cls,Date_of_birth,gender):
        weeks = (abs(Date_of_birth-date.today()).days)/7
        return cls.query.filter_by(Age = round(weeks),gender=gender).first()
        
    def get_height_status(self,height):
        return get_status(self.lowest_height,self.highest_height,height)
    
    def get_weight_status(self,weight):
        return get_status(self.lowest_weight,self.highest_weight,weight)

            


    

   
