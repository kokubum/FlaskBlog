from datetime import timedelta
import os

#Directory that the database will be saved
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REMEMBER_COOKIE_DURATION = os.environ.get('REMEMBER_COOKIE_DURATION',timedelta(minutes=5))
    

    #Email Configuration
    MAIL_PORT = int(os.environ.get('MAIL_PORT','587'))
    MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.googlemail.com')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS','true').lower() in ['true','on','1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SENDER = '[ADMIN]<admin@blog.com>'
    
    ADMIN_BLOG = os.environ.get('ADMIN_BLOG')
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE','20'))
    FOLLOWERS_PER_PAGE = int(os.environ.get('FOLLOWERS_PER_PAGE','20'))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL','sqlite:///' + os.path.join(base_dir,'data-dev.sqlite'))


class TestingConfig(Config):
    TESTING = True
    #In-Memory database
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL','sqlite://')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL','sqlite:///' + os.path.join(base_dir,'data-prod.sqlite'))

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,

    'default':DevelopmentConfig
}