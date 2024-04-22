from flask import Flask
from flask_restful import Api 
from model.mother import MotherModel
from resources.mother import MotherRegister,MotherLogin,MotherVerification,MotherLogout,MotherDelete,FacebookLogin
from resources.articles import MotherArticles,MotherArticle,BabyArtical,BabyArticals
from resources.doctors import AllDoctors,DoctorResource
from resources.favorite import favoriteArticalsResource,favoriteVideoResource,favoriteBabyArticalsResource
from resources.child import ChildsResource,ChildResource
from resources.configurations import configuraitons,ResetEmail,ResetPassword,configuraitonsForbaby,babyheight,babyweight
from resources.videos import VideosResource
from resources.event import EventsResource,EventResource
from resources.Games import gamesResult
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:FarOuQ_2022@localhost:3306/users'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.secret_key = "kidzy1192"
app.config.from_pyfile("config.cfg")
api.add_resource(MotherRegister, '/user/signup')
api.add_resource(MotherLogin, '/user/login')
api.add_resource(MotherVerification, '/verification/<token>')
api.add_resource(MotherArticles, '/articals')
api.add_resource(MotherArticle, '/artical/<int:id>')
api.add_resource(MotherDelete,'/user/delete')
api.add_resource(AllDoctors, '/doctors')
api.add_resource(DoctorResource, '/doctor/<int:doctor_id>')
api.add_resource(favoriteArticalsResource, '/favorite/artical')
api.add_resource(favoriteVideoResource, '/favorite/video')
api.add_resource(ChildsResource, '/child')
api.add_resource(ChildResource,'/child/<int:child_id>')
api.add_resource(configuraitons, '/configuration')
api.add_resource(configuraitonsForbaby, '/confbaby/<int:child_id>')
api.add_resource(babyweight, '/babyweight/<int:child_id>')
api.add_resource(babyheight, '/babyheight/<int:child_id>')
api.add_resource(MotherLogout, '/user/logout')
api.add_resource(ResetPassword, '/user/resetpassword')
api.add_resource(ResetEmail, '/user/resetemail')
api.add_resource(VideosResource,'/videos')
api.add_resource(EventsResource,'/events/<int:child_id>')
api.add_resource(EventResource,'/event/<int:event_id>')
api.add_resource(gamesResult,'/result/<int:game_number>/<int:child_id>')
api.add_resource(BabyArticals, '/baby_articals/<int:child_id>')
api.add_resource(BabyArtical, '/baby_artical/<int:id>')
api.add_resource(favoriteBabyArticalsResource, '/fav_baby_artical/<int:child_id>')
api.add_resource(FacebookLogin,'/facebook/login')


@app.before_first_request
def create_all():
    db.create_all()
 
@jwt.user_identity_loader
def user_identity_lookup(identity):
    return identity

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return MotherModel.find_by_id(identity)

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload:dict):
    return jwt_payload['jti'] in BLACKLIST


if __name__ == '__main__':
    from db import db 
    db.init_app(app)
    from resources.mother import mail 
    mail.init_app(app)
    app.run(debug = True)