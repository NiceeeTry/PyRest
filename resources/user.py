from flask import request, url_for, render_template
from flask_restful import Resource
from http import HTTPStatus
from utils import generate_token, verify_token, save_image
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.user import UserSchema
from schemas.recipe import RecipeSchema
from webargs import fields
from webargs.flaskparser import use_kwargs
from models.recipe import Recipe
from mailgun import MailgunApi
import os
from dotenv import load_dotenv
from extensions import image_set


load_dotenv()

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email',))
recipe_list_schema = RecipeSchema(many=True)
mailgun = MailgunApi(domain=os.environ.get('MAILGUN_DOMAIN'),
                     api_key=os.environ.get('MAILGUN_API_KEY'))

user_avatar_schema=UserSchema(only=('avatar_url',))

class UserListResource(Resource):
    def post(self):

        json_data = request.get_json()

        data = user_schema.load(data=json_data)
        try:
            data = user_schema.load(data=json_data)
        except Exception as err:
            errors = err.messages
            return {"message":"Validation errors",'errors':errors}, HTTPStatus.BAD_REQUEST
       

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()
        token = generate_token(user.email, salt='activate')
        subject = 'Please confirm your registration.'
        link = url_for('useractivateresource', token=token, _external=True)
        text = 'Hi, Thanks for using SmileCook! Please confirm your registration by clicking on the link: {}'.format(link)
        # mailgun.send_email(to=user.email, subject=subject, text=text,
        #                    html=render_template('email/confirmation.html', link=link))
        

        return user_schema.dump(user), HTTPStatus.CREATED
        # username = json_data.get('username')
        # # print(username)
        # email = json_data.get('email')
        # # print(email)
        # non_hash_password = json_data.get('password')
        # # print(non_hash_password)
        # if User.get_by_username(username):
        #     return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        # if User.get_by_email(email):
        #     return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        # password = hash_password(non_hash_password)

        # user = User(
        #     username=username,
        #     email=email,
        #     password=password
        # )

        # user.save()

        # data = {
        #     'id': user.id,
        #     'username': user.username,
        #     'email': user.email
        # }

        # return data, HTTPStatus.CREATED

class UserResource(Resource):
    @jwt_required(optional=True)
    def get(self, username):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message':'user not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        if current_user == user.id:
            data= user_schema.dump(user)
        else:
            data = user_public_schema.dump(user)
        return data, HTTPStatus.OK
    
class MeResource(Resource):
    @jwt_required()
    def get(self):
        user = User.get_by_id(id = get_jwt_identity())
        return user_schema.dump(user), HTTPStatus.OK
    
class UserRecipeListResource(Resource):
    @jwt_required(optional=True)
    @use_kwargs({'visibility':fields.Str()})
    def get(self, username, visibility='all'):
        print(visibility,'--------------')
        user = User.get_by_username(username=username)
        if user is None:
            return {'message':'User not found'},HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'
        print(visibility,'-----------------------',current_user, user.id)
        recipes = Recipe.get_all_by_user(user_id=user.id, visibility=visibility)
        return recipe_list_schema.dump(recipes), HTTPStatus.OK
    
class UserActivateResource(Resource):
    def get(self, token):
        email = verify_token(token, salt='activate')
        if email is False:
            return {'message':'Invalid token or token expired'}, HTTPStatus.BAD_REQUEST
        
        user = User.get_by_email(email=email)
        if not user:
            return {'message':'User not found'}, HTTPStatus.NOT_FOUND
        
        if user.is_active is True:
            return {'message':'The user account is already activated'}, HTTPStatus.BAD_REQUEST
        
        user.is_active = True
        user.save()
        return {}, HTTPStatus.NO_CONTENT
    
class UserAvatarUploadResource(Resource):
    @jwt_required()
    def put(self):
        # print("i was here -----------------------")
        file = request.files.get('avatar')
        if not file:
            return {'message':'Not a valid image'},HTTPStatus.BAD_REQUEST
        
        if not image_set.file_allowed(file,file.filename):
            return {'message':'File type not allowed'}, HTTPStatus.BAD_REQUEST
        # print(file,"----------------------------------------------------")
        user = User.get_by_id(id=get_jwt_identity())
        if user.avatar_image:
            avatar_path=image_set.path(folder='avatars',filename=user.avatar_image)
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
        filename = save_image(image=file,folder='avatars')
        user.avatar_image = filename
        user.save()
        return user_avatar_schema.dump(user),HTTPStatus.OK