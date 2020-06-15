from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import  Moment
from flask_migrate import Migrate
from flask_login import LoginManager

bootstrap=Bootstrap()
db=SQLAlchemy()
moment=Moment()
ckeditor=CKEditor()
mail=Mail()
migrate=Migrate()
login_manager=LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from myblog.models import Admin
    user=Admin.query.get(int(user_id))
    return user
