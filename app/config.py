import os

from dotenv import load_dotenv

app_root = os.path.join(os.path.dirname(__file__), "..")
dotenv_path = os.path.join(app_root, ".env")


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class Production(Config):
    DEBUG = False


class Development(Config):
    DEVELOPMENT = True
    DEBUG = True


class Testing(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")


app_configuration = {
    "production": Production,
    "development": Development,
    "testing": Testing,
}
