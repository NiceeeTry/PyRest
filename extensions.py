from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_uploads import UploadSet, IMAGES
from flask_caching import Cache


cache = Cache()
image_set  = UploadSet('images',IMAGES)

jwt = JWTManager()
db = SQLAlchemy()