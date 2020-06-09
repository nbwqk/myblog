from myblog.extensions import db
from datetime import datetime

class Admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20))
    password_hash=db.Column(db.String(128))
    blog_title=db.Column(db.String(60))
    blog_sub_title=db.Column(db.String(100))
    name=db.Column(db.String(30))
    about=db.Column(db.Text)

class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=True)
    posts=db.relationship('Post',back_populates='category')

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(60))
    body=db.Column(db.Text)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)
    can_comment=db.Column(db.Boolean,default=True)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    category=db.relationship('Category',back_populates='posts')
    comments=db.relationship('Comment',backref='post',cascade='all,delete-orphan')

class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    author=db.Column(db.String(30))
    email=db.Column(db.String(254))
    site=db.Column(db.String(255))
    body=db.Column(db.Text)
    from_admin=db.Column(db.Boolean,default=False) # 评论是否来自于管理员
    reviewed=db.Column(db.Boolean,default=False)   # 判断评论是否通过审查
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))

    #post=db.relationship('Post',back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all')
    replied=db.relationship('Comment',back_populates='replies',remote_side=[id])
