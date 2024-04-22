from db import db
from passlib.hash import pbkdf2_sha256

class MotherModel(db.Model):
    __tablename__ = 'Mother'

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(60))
    password = db.Column(db.String(320))
    facebook = db.Column(db.Boolean)
    children = db.relationship('childModel',backref = 'child')

    def __init__(self, firstname, email,password,lastname=None):
        self.first_name = firstname
        self.last_name = lastname
        self.email = email 
        self.password = pbkdf2_sha256.hash(password)
    
    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email = email).first()

    @classmethod 
    def find_by_id(cls,id):
        return cls.query.filter_by(id = id).first()
    
    def json(self):
        return{"firstname":self.first_name,"lastname":self.last_name,"email":self.email,"password":self.password}
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
       


    