from flask_restful import Resource,reqparse
from model.doctors import Doctor,Professions
from model.reviews import Review
from flask_jwt_extended import jwt_required,current_user
from flask import request


class AllDoctors(Resource):

    @jwt_required()
    def get(self):
        return {"Doctors":[item.json() for item in Doctor.find_all()]}


class DoctorResource(Resource):

    @jwt_required()
    def get(self,doctor_id):
        doctor = Doctor.find_by_id(doctor_id)   
        all_reviews = Review.find_all_reviews(doctor_id)
        return {"doc info":doctor.show_all(), "reviews":[review.json() for review in all_reviews]}

    @jwt_required()
    def post(self,doctor_id):
        data = request.get_json(force=True)
        review = Review(content=data["content"], rating=data["rating"], doctor_id=doctor_id, mother_name=current_user.firstname)  
        review.save_to_db()
        return {"message" : True}   



