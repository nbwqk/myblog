from flask import Flask,render_template
from myblog.blueprints.auth import auth_bp
from myblog.blueprints.admin import admin_bp
from myblog.blueprints.blog import blog_bp
from myblog.settings import config
from myblog.extensions import bootstrap,mail,moment,db,ckeditor,migrate
from myblog.models import Admin,Category,Post,Comment
import os,click

def create_app(config_name=None):
    if config_name is None:
        config_name=os.getenv('FLASK_CONFIG','development')

    app=Flask('myblog')
    app.config.from_object(config[config_name])

    register_logging(app) # 注册日志处理器
    register_extensions(app) # 注册扩展（扩展初始化）
    register_blueprints(app) # 注册蓝本
    register_commands(app) # 注册自定义shell命令
    register_errors(app) #注册错误处理函数
    register_shell_content(app) # 注册shell上下文处理函数
    register_template_context(app) # 注册模板上下文处理函数
    return app

def register_logging(app):
    pass

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    migrate.init_app(app,db)

def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

def register_shell_content(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin=Admin.query.first()
        categories=Category.query.order_by(Category.name).all()
        return dict(admin=admin,categories=categories)

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'),400

def register_commands(app):
    @app.cli.command()
    @click.option('--category',default=10,help='Quantity of categories,default is 10.')
    @click.option('--post', default=50, help='Quantity of post,default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments,default is 500.')
    def forge(category,post,comment):
        """Generate fake data."""
        from myblog.fakes import fake_admin,fake_categories,fake_posts,fake_comments

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Genertaing %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done.')
