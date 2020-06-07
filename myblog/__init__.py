from flask import Flask
from myblog.blueprints.auth import auth_bp
from myblog.blueprints.admin import admin_bp
from myblog.blueprints.blog import blog_bp
from myblog.settings import config
import os

def create_app(config_name=None):
    if config_name is None:
        config_name=os.getenv('FLASK_CONFIG','development')

    app=Flask('myblog')
    app.config.from_object(config[config_name])

    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(auth_bp,url_prefix='/auth')
    return app

