from model.articles import ArticlesModel
from model.favorite import FavoriteArtical
from model.child import ChildModel
from flask_restful import Resource
import docx2txt
from flask_jwt_extended import jwt_required
from datetime import date

class MotherArticles(Resource):
    
    @jwt_required()
    def get(self): 
        articles = ArticlesModel.display_favorites_and_normal()
        lis = list()
        for article in articles:
            lis.append({'id':article.id,
            'title':article.title,
            'publish_date':article.publish_date,
            'website':article.website_taken_from,
            'for_age':article.for_age,
            'favorite':article.fa})
        return {"articals":lis}
        
    
class MotherArticle(Resource):
    
    @jwt_required()
    def get(self,id):
        artical = ArticlesModel.find_by_id(id)
        my_text = docx2txt.process(artical.Content)
        x = my_text.replace("\n","")
        return {
        "id":artical.id,
        "title":artical.title,
        "publish_date":artical.publish_date,
        "website":artical.website_taken_from,
        "for_age":artical.for_age,
        "Content":x}

class BabyArticals(Resource):
    @jwt_required()
    def get(self,child_id):
        child = ChildModel.find_child(child_id=child_id)
        weeks = (abs(child.date_of_birth-date.today()).days)/7
        articles = ArticlesModel.display_favorites_and_normal_for_children(child_id,round(weeks/4))
        lis = list()
        for article in articles:
            lis.append({'id':article.id,
            'title':article.title,
            'publish_date':article.publish_date,
            'website':article.website_taken_from,
            'for_age':article.for_age,
            'favorite':article.fa
            })
        return {"articals":lis}
    
class BabyArtical(Resource):
    
    @jwt_required()
    def get(self,id):
        article = ArticlesModel.find_by_id(id)
        my_text = docx2txt.process(article.Content)
        x = my_text.replace("\n","")
        return {
        "id":article.id,
        "title":article.Title,
        "publish_date":article.publish_date,
        "website":article.website_taken_from,
        "for_age":article.for_age,
        "Content":x}