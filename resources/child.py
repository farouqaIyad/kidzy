from flask_restful import Resource
from model.child import ChildModel
from flask_jwt_extended import jwt_required,current_user
from flask import request


class ChildsResource(Resource):

    @jwt_required()
    def post(self):
        data = request.get_json(force=True)
        child = ChildModel(**data, mother_id=current_user.id)
        child.save_to_db()
        return {"message":True}

    @jwt_required()
    def get(self):
        children = current_user.children
        if children:
            return {"childs":[{'id':child.id,'name':child.name,'gender':child.gender} for child in children]}
        else:
            return{"childs":[]}
    
    @jwt_required()
    def update(self):
        children = ChildModel.find_child(current_user.id)
    

class ChildResource(Resource):
    
    @jwt_required()
    def delete(self,child_id):
        child = ChildModel.find_child(child_id=child_id)
        if child:
            child.delete_from_db()
            return {"message":True}
        else:
            return {"message":False}
    
    @jwt_required()
    def update(self,child_id):
        child = ChildModel.find_child(child_id=child_id)


