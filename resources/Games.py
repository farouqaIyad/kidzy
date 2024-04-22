from flask_restful import Resource,reqparse
from model.games import GamesModel
from flask import request

class gamesResult(Resource):
    
   
    def post(self,game_number,child_id):
        data = request.get_json(force=True)
        result = GamesModel(data['success'],game_number,data['Date'],data['begin_time'],data['duration'],child_id)
        result.save_to_db()
        return {"message":True}
    

    def get(self,game_number,child_id):
        result = GamesModel.find(game_number, child_id)
        return {"result":[item.json() for item in result]}
