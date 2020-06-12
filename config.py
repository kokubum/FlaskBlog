import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY','random_secret_key')


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True


config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,

    'default':DevelopmentConfig
}