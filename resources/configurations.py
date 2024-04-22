from flask_restful import Resource
from flask_jwt_extended import jwt_required,current_user
from passlib.hash import pbkdf2_sha256
from flask import request
from model.child import ChildModel,averageChild
from flask_mail import Mail,Message
mail = Mail()

class configuraitons(Resource):
    
    @jwt_required()
    def get(self):
        return {"mother":current_user.json()}
        
    @jwt_required()
    def post(self):
        data = request.get_json(force=True)
        current_user.firstname = data["firstname"]
        current_user.lastname = data["lastname"]
        current_user.save_to_db()
        return {"message":True}



class configuraitonsForbaby(Resource):
    
    @jwt_required()
    def get(self,child_id):
        child = ChildModel.find_child(child_id=child_id)
        average = averageChild.find_data(child.date_of_birth,child.gender)
        if average:
            return {"baby":child.json(),"height":average.get_height_status(child.height),"weight":average.get_weight_status(child.weight)}
        else: 
            return{"baby":child.json(),"height":None,"weight":None}



class babyheight(Resource):
    @jwt_required()
    def post(self,child_id):
        child = ChildModel.find_child(child_id=child_id)
        data = request.get_json(force=True)
        child.height = data["height"]
        child.save_to_db()
        return {"message":True}



class babyweight(Resource):
    @jwt_required()
    def post(self,child_id):
        child = ChildModel.find_child(child_id=child_id)
        data = request.get_json(force=True)
        child.weight = data["weight"]
        child.save_to_db()
        return {"message":True}



class ResetPassword(Resource):
   
    @jwt_required()
    def post(self):
        data = request.get_json(force=True)
        print(data['old_password'])
        print(data['new_password'])

        if pbkdf2_sha256.verify(data["old_password"],current_user.password):
            current_user.password =pbkdf2_sha256.hash(data["new_password"])
            current_user.save_to_db()
            print(current_user.password)
            return {"message":True}
        else:
            return {"message":"كلمة السر خاطئة"}



class ResetEmail(Resource):
    

    @jwt_required()
    def post(self):
        data = request.get_json(force=True)
        if pbkdf2_sha256.verify(data['password'], current_user.password):
            current_user.email = data["email"]
            current_user.save_to_db()
            return {"message":True}
        else:
            return{"message":False}
        
        
        