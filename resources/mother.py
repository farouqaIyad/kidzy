from flask_restful import Resource
from model.mother import MotherModel
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,jwt_required,get_jwt,current_user
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_mail import Mail,Message
from flask import url_for,render_template,request,make_response
from blacklist import BLACKLIST
from email_validator import validate_email, EmailNotValidError
s =URLSafeTimedSerializer(secret_key='kidzy1192')
mail = Mail()


class FacebookLogin(Resource):

    def post(self):
        data = request.get_json(force=True)
        mother = MotherModel.find_by_email(data['email'])
        if mother:
            access_token = create_access_token(identity=mother.id, fresh = True)
        else:
            mother = MotherModel(**data)
            mother.facebook = True
            mother.save_to_db()
            access_token = create_access_token(identity=mother.id, fresh = True)

        return {"message":True,"access_token":access_token}
            


class MotherRegister(Resource):

    def post(self):
        data = request.get_json(force=True)
        try:
            v = validate_email(data["email"])
        except EmailNotValidError as e:
            return {"message":str(e)}
        if MotherModel.find_by_email(data["email"]):
            return {"message":"المستخدم مسجل مسبقا"}
        else:
            global Mother
            Mother = MotherModel(**data)
            token = s.dumps(Mother.email, salt= 'email-confirm')
            msg = Message("[Kidzy] Confirm your account", sender='kidzyApp1@outlook.com', recipients=[Mother.email])
            link = url_for('motherverification', token = token, _external= True)
            msg.body = 'your link is {}'.format(link)
            msg.html = render_template('index.html', link=link, name = Mother.first_name)
            mail.send(msg)
        return {"message":True}


class MotherVerification(Resource):

    def get(self,token):
        
        try:
            email = s.loads(token, salt='email-confirm', max_age=600)
            Mother.save_to_db()
        except SignatureExpired:
            return {"message":False}
        response = make_response(render_template('verification.html'))
        return response


class MotherLogin(Resource):
   

    def post(self):
        data = request.get_json(force=True)
        try:
            v = validate_email(data["email"])
        except EmailNotValidError as e:
            return {"message":"البريد الإلكتروني خاطئ"}
        Mother = MotherModel.find_by_email(data["email"])
        if Mother:
            if not Mother.facebook:
                if  pbkdf2_sha256.verify(data['password'], Mother.password):
                    access_token = create_access_token(identity=Mother.id, fresh = True)
                    return {"message":True, "access_token":access_token,
                    "firstname":Mother.firstname,"lastname":Mother.lastname,"email":Mother.email,}
                else:
                    return {"message":"كلمة السر خاطئة "}
            else:
                return {"message":"الحساب مسجل عبر فيسبوك"}
        else:
            return {"message":"الحساب ليس موجود "}


class MotherLogout(Resource):
    
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        print(jti)
        BLACKLIST.add(jti)
        return {"message":True}


class MotherDelete(Resource):

    @jwt_required()
    def delete(self):
        current_user.delete_from_db()
        return {"message":True}
        
