from db import db 
from model.favorite import FavoriteArtical
from flask_jwt_extended import current_user

class ArticlesModel(db.Model):
    __tablename__ = 'articals'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    publish_date = db.Column(db.DateTime)
    for_age = db.Column(db.Integer)
    website_taken_from = db.Column(db.String(50))
 
    def json(self):
        return {
            "id":self.id,
            "title":self.title,
            "publish_date":self.publish_date,
            "web_site":self.website_taken_from,
            "for_age":self.for_age
        }

    @classmethod
    def display_favorites_and_normal(cls):
        result = db.session.execute('select articals.id,articals.title,articals.publish_date,articals.website_taken_from,articals.for_age,s.fa from articals join(select articals.id na ,count(fav.id) fa from articals left join fav on fav.favorite_id = articals.id and fav.user_id = :val group by articals.id) s on s.na = articals.id',{'val':current_user.id}).all()
        return result
    
    @classmethod
    def display_favorites_and_normal_for_children(cls,child_id,age):
        result = db.session.execute('select articals.id,articals.title,articals.publish_date,articals.website_taken_from,articals.for_age,s.fa from articals join(select articals.id na ,count(baby_fav.id) fa from articals left join baby_fav on baby_fav.Art_id = articals.id and baby_fav.child_id = :val group by articals.id) s on s.na = articals.id where articals.for_age = :age;)',{'val':child_id,'age':age}).all()
        return result

    @classmethod
    def find_all(cls):
        return cls.query.all()
        
    @classmethod
    def find_by_id (cls,id):
        return cls.query.filter_by(id = id).first()
        
    @classmethod 
    def find_related_to_age(cls,age_in_weeks):
        months = age_in_weeks /4
        return cls.query.filter_by(for_age = round(months)).all()


