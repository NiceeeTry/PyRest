class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:qwerty@:5436/smilecook'
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY ='super-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    
    