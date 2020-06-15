from myblog.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class Admin(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20))
    password_hash=db.Column(db.String(128))
    blog_title=db.Column(db.String(60))
    blog_sub_title=db.Column(db.String(100))
    name=db.Column(db.String(30))
    about=db.Column(db.Text)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=True)
    posts=db.relationship('Post',back_populates='category')

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)  # 帖子ID
    title=db.Column(db.String(60))             # 帖子标题
    body=db.Column(db.Text)                    # 帖子正文
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)   # 发帖时间
    can_comment=db.Column(db.Boolean,default=True)             # 帖子是否可评论
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))  # 帖子的类别，外键
    category=db.relationship('Category',back_populates='posts')     # 帖子所属的类别集合（单数）
    comments=db.relationship('Comment',back_populates='post',cascade='all,delete-orphan') # 帖子所属的评论集合（复数)

class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)  # 评论ID
    author=db.Column(db.String(30))            # 评论作者
    email=db.Column(db.String(254))            # 评论作者邮箱
    site=db.Column(db.String(255))             # 评论作者网址
    body=db.Column(db.Text)                    # 评论内容
    from_admin=db.Column(db.Boolean,default=False) # 评论是否来自于管理员
    reviewed=db.Column(db.Boolean,default=False)   # 判断评论是否通过审查
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True) # 评论发出时间
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))  # 评论所属的帖子ID，外键
    post=db.relationship('Post',back_populates='comments')  # 评论所属的帖子集合（单数）
    replied_id=db.Column(db.Integer,db.ForeignKey('comment.id')) # 所回复的那个评论ID
    replied=db.relationship('Comment',back_populates='replies',remote_side=[id]) # 被回复评论的集合（单数）
    replies=db.relationship('Comment',back_populates='replied',cascade='all')    # 回复评论的评论集合（复数）