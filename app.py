from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db, jwt, image_set, cache, limiter

from resources.user import UserListResource, UserResource, MeResource, UserRecipeListResource, UserActivateResource,UserAvatarUploadResource
from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource, RecipeCoverUploadResource

from resources.token import TokenResource, RefreshResourse,RevokeResource, black_list
from flask_uploads import configure_uploads, patch_request_class

import os

def create_app(config_str = 'config.DevelopmentConfig'):
    # env = os.environ.get('ENV','Testing')
    # if env=='Production':
    #     config_str = 'config.ProductionConfig'
    # elif env == 'Staging':
    #     config_str = 'config.StagingConfig'
    # elif env =='Testing':
    #     config_str = 'config.TestConfig'
    # else:
    #     config_str = 'config.DevelopmentConfig'
    app =  Flask(__name__)
    app.config.from_object(config_str)
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()
    migrate = Migrate(app,db)
    jwt.init_app(app)
    configure_uploads(app,image_set)
    patch_request_class(app,10*1024*1024)
    cache.init_app(app)
    limiter.init_app(app)
    with app.app_context():
        db.create_all()
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list
    # @jwt.token_in_blocklist_loader
    # def check_if_token_revoked(jwt_header, jwt_payload):
    #     jti = jwt_payload["jti"]
    #     token = db.session.query().filter_by(jti=jti).scalar()
    #     return token is not None
    
    # @app.before_request
    # def before_request():
    #     print('\n====================BEFORE REQUEST====================\n')
    #     print(cache.cache._cache.keys())
    #     print('\n======================================================\n')
    
    # @app.after_request
    # def after_request(response):
    #     print('\n====================AFTER REQUEST====================\n')
    #     print(cache.cache._cache.keys())
    #     print('\n======================================================\n')
    #     return response
        
def register_resources(app):
    api = Api(app)
    
    api.add_resource(MeResource,'/me')
    
    api.add_resource(UserListResource,'/users')
    api.add_resource(UserResource,'/users/<string:username>')
    api.add_resource(UserRecipeListResource, '/users/<string:username>/recipes')
    api.add_resource(UserActivateResource, '/users/activate/<string:token>')
    api.add_resource(UserAvatarUploadResource, '/users/avatar')
    
    api.add_resource(TokenResource,'/token')
    api.add_resource(RefreshResourse,'/refresh')
    api.add_resource(RevokeResource,'/revoke')
    
    api.add_resource(RecipeListResource,'/recipes')
    api.add_resource(RecipeResource,'/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource,'/recipes/<int:recipe_id>/publish')
    api.add_resource(RecipeCoverUploadResource, '/recipes/<int:recipe_id>/cover')


if __name__=='__main__':
    app = create_app()
    app.run(port=5000, debug=True)