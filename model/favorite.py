from db import db 
from flask_jwt_extended import current_user

class FavoriteArtical(db.Model):
    __tablename__ = 'fav'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('Mother.id'))
    favorite_id = db.Column(db.Integer, db.ForeignKey('articals.id'))

    def __init__(self,user_id,favorite_id):
        self.user_id = user_id
        self.favorite_id = favorite_id

    @classmethod
    def find_all(cls):
        result = db.session.execute('select id,title,publish_date,for_age,website_taken_from from articals where articals.id in (select favorite_id from fav where fav.user_id= :val)',{'val':current_user.id}).all()
        return result

    @classmethod
    def find_one(cls,artical_id):
        return cls.query.filter_by(user_id = current_user.id,favorite_id = artical_id ).first()
            
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def json(self):
        return{"artical_id":self.favorite_id}
    

class FavoriteArticalBaby(db.Model):
    __tablename__ = 'baby_favorite'

    id = db.Column(db.Integer, primary_key = True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    Art_id = db.Column(db.Integer, db.ForeignKey('articals.id'))

    def __init__(self,child_id,favorite_id):
        self.child_id = child_id
        self.Art_id = favorite_id

    @classmethod
    def find_one(cls,child_id,artical_id):
        return cls.query.filter_by(child_id = child_id,Art_id = artical_id ).first()
            
    @classmethod
    def find_all(cls,child_id):
        result = db.session.execute('select id,title,publish_date,for_age,website_taken_from from articals where articals.id in (select id from baby_fav where baby_fav.child_id=:val)',{'val':child_id}).all()
        return result
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def json(self):
        return{"artical_id":self.Art}


class Favoritevideo(db.Model):
    __tablename__ = 'favorite_video'

    id = db.Column(db.Integer, primary_key = True)
    favorited_video_id = db.Column(db.Integer, db.ForeignKey('videos_for_babies.video_id'))
    user_favorited_id = db.Column(db.Integer, db.ForeignKey('Mother.id'))

    def __init__(self,user_id,favorite_id):
        self.user_favorited_id = user_id
        self.favorited_video_id = favorite_id

    @classmethod
    def find_all(cls):
        result = db.session.execute('select video_id,title,video_link,image from videos_for_babies where videos_for_babies.video_id in (select favorited_video_id from favorite_video where favorite_video.user_favorited_id= :val)',{'val':current_user.id}).all()
        return result
    
    @classmethod
    def find_one(cls,video_id):
        return cls.query.filter_by(user_favorited_id = current_user.id,favorited_video_id = video_id ).first()
            
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def json(self):
        return{"video_id":self.favorite_id}

