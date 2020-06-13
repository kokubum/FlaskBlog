import os

#Directory that the database will be saved
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY','secret_key')

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