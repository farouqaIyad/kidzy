from flask_restful import Resource
from flask_jwt_extended import jwt_required
from model.videos import VideosModel

class VideosResource(Resource):

    @jwt_required()
    def get(self):
        videos = VideosModel.display_favorites_and_normal()
        lis = list()
        for video in videos:
            lis.append({'id':video.video_id,
            'title':video.title,
            'video_link':video.video_link,
            'image':video.image,
            'favorite':video.fa})
        return {"videos":lis}
        
