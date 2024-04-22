from flask_restful import Resource,reqparse
from model.favorite import FavoriteArtical,Favoritevideo,FavoriteArticalBaby
from model.articles import ArticlesModel
from flask_jwt_extended import current_user,jwt_required
from flask import request

class favoriteArticalsResource(Resource):

    @jwt_required()
    def get(self):   
        articles = FavoriteArtical.find_all()
        lis = list()
        for article in articles:
            lis.append({'id':article.id,
            'title':article.title,
            'publish_date':article.publish_date,
            'website':article.website_taken_from,
            'for_age':article.for_age,
            })
        return {"articals":lis}
    
    @jwt_required()
    def post(self):
        data = request.get_json(force=True)
        favorite_artical = FavoriteArtical.find_one(data['artical_id'])
        if favorite_artical:
            favorite_artical.delete_from_db()
            return {"message":True}
        favorite_artical = FavoriteArtical(current_user.id, data['artical_id'])
        favorite_artical.save_to_db()
        return {"message":True}

class favoriteBabyArticalsResource(Resource):

    @jwt_required()
    def get(self,child_id):   
        articles = FavoriteArticalBaby.find_all(child_id=child_id)
        lis = list()
        for article in articles:
            lis.append({'id':article.id,
            'title':article.title,
            'publish_date':article.publish_date,
            'website':article.website_taken_from,
            'for_age':article.for_age,
            })
        return {"articals":lis}
    
    @jwt_required()
    def post(self,child_id):
        data = request.get_json(force=True)
        favorite_artical = FavoriteArticalBaby.find_one(child_id,data['artical_id'])
        if favorite_artical:
            favorite_artical.delete_from_db()
            return {"message":True}
        favorite_artical = FavoriteArticalBaby(child_id, data['artical_id'])
        favorite_artical.save_to_db()
        return {"message":True}

class favoriteVideoResource(Resource):

    @jwt_required()
    def get(self):   
        videos = Favoritevideo.find_all()
        lis = list()
        for video in videos:
            lis.append({'id':video.video_id,
            'title':video.title,
            'website':video.video_link,
            'image':video.image,
            })
        return {"videos":lis}
    
    @jwt_required()
    def post(self):
        data = request.get_json(force=True)
        favorite_video = Favoritevideo.find_one(data['video_id'])
        if favorite_video:
            favorite_video.delete_from_db()
            return {"message":True}
        favorite_video = Favoritevideo(current_user.id, data['video_id'])
        favorite_video.save_to_db()
        return {"message":True}


    

        
        


