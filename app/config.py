
import os

from dotenv import load_dotenv

app_root = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(app_root, '.env')


class Config(object):
	DEBUG = False
	TESTING = False
	SECRET_KEY = os.getenv('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class ProductionConfig(Config):
	DEBUG = False

class StagingConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
	DEBUG=True
	SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')

app_configuration = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
