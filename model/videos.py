from db import db 
from flask_jwt_extended import current_user

class VideosModel(db.Model):
    __tablename__ = 'videos_for_babies'
    video_id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100))
    video_link = db.Column(db.String(50))
    image = db.Column(db.String(100))

    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_id(cls,video_id):
        return cls.query.filter_by(video_id = video_id).first()

    
    @classmethod
    def display_favorites_and_normal(cls):
        result = db.session.execute('select videos_for_babies.video_id,videos_for_babies.title,videos_for_babies.video_link,videos_for_babies.image,s.fa from videos_for_babies join(select videos_for_babies.video_id na ,count(favorite_video.id) fa from videos_for_babies left join favorite_video on favorite_video.favorited_video_id = videos_for_babies.video_id and favorite_video.user_favorited_id = :val group by videos_for_babies.video_id) s on s.na = videos_for_babies.video_id',{'val':current_user.id}).all()
        return result

    def json(self):
        return {"id":self.video_id, "title":self.title, 
        "video_link":self.video_link, "publish_date":self.publish_date,
        "for_age":self.for_age}