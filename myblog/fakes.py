from myblog.models import Admin,Category,Post,Comment
from myblog.extensions import db
from faker import Faker
import random

fake=Faker()

def fake_admin():                 # 生成虚拟管理员
    admin=Admin(username='admin',
                blog_title='Myblog',
                blog_sub_title="No.I'm the real thing.",
                name='Mima Kirigoe',
                about='Um,I,Mima Kirigoe,had a fun times as a member of CHAM...')
    db.session.add(admin)
    db.session.commit()

def fake_categories(count=10):        # 生成虚拟分类
    category=Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category=Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_posts(count=50):                   # 生成虚拟文章
    for i in range(count):
        post=Post(title=fake.sentence(),
                  body=fake.text(2000),
                  category=Category.query.get(random.randint(1,Category.query.count())),
                  timestamp=fake.date_time_this_year()
                  )
        db.session.add(post)
    db.session.commit()

def fake_comments(count=500):
    for i in range(count):                    # 添加已审核的评论
        comment=Comment(author=fake.name(),
                        email=fake.email(),
                        site=fake.url(),
                        body=fake.sentence(),
                        timestamp=fake.date_time_this_year(),
                        reviewed=True,
                        post=Post.query.get(random.randint(1,Post.query.count()))
                        )
        db.session.add(comment)

    salt=int(count*0.1)
    for i in range(salt):                 # 添加未审核通过的评论
        comment = Comment(author=fake.name(),
                          email=fake.email(),
                          site=fake.url(),
                          body=fake.sentence(),
                          timestamp=fake.date_time_this_year(),
                          reviewed=False,
                          post=Post.query.get(random.randint(1, Post.query.count()))
                          )
        db.session.add(comment)

        comment = Comment(author='Mima Kirigoe',    # 添加管理员发表的评论
                          email='nbyzwqk@163.com',
                          site='163.com',
                          body=fake.sentence(),
                          timestamp=fake.date_time_this_year(),
                          from_admin=True,
                          reviewed=True,
                          post=Post.query.get(random.randint(1, Post.query.count()))
                          )
        db.session.add(comment)
    db.session.commit()

    for i in range(salt):                   # 添加回复
        comment=Comment(author=fake.name(),
                        email=fake.email(),
                        site=fake.url(),
                        body=fake.sentence(),
                        timestamp=fake.date_time_this_year(),
                        reviewed=True,
                        replied=Comment.query.get(random.randint(1,Comment.query.count())),
                        post=Post.query.get(random.randint(1,Post.query.count()))
                        )
        db.session.add(comment)
    db.session.commit()

