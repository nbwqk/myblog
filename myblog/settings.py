import os

basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class BaseConfig(object):
    SECRET_KEY=os.getenv('SECRET_KEY','secret string')

    SQLALCHEMY_TRACK_MODIFICATIONS=False

    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER=('Myblog',MAIL_USERNAME)

    MYBLOG_EMAIL=os.getenv('MYBLOG_EMAIL')
    MYBLOG_POST_PER_PAGE=10
    MYBLOG_MANAGE_POST_PER_PAGE=15
    MYBLOG_COMMENT_PER_PAGE=15
    # （‘theme name','display name')
    MYBLOG_THEMES={'perfect_blue':'Perfect Blue','black_swan':'Black Swan'}

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'data-dev.db')

class TestingConfig(BaseConfig):
    TESTING=True
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'  # in-memory database

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI','sqlite:///'+os.path.join(basedir,'data.db'))

config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig
}