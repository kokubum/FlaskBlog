from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User,Post,Comment
from datetime import datetime

def users(count=100):
    fake = Faker()
    i = 0

    while i<count:
        u = User(
            email = fake.email(),
            username = fake.user_name(),
            password = 'password',
            confirmed = True,
            name = fake.name(),
            location = fake.city(),
            about_me = fake.text(),
            member_since = fake.past_date()
        )
   
        db.session.add(u)
        try:
            db.session.commit()
            i+=1
        except IntegrityError:
            db.session.rollback()


def posts(count = 100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0,user_count-1)).first()
        p = Post(
            title = fake.sentence(),
            body = fake.text(max_nb_chars=500),
            time_stamp = fake.date_time_between(u.member_since,datetime.utcnow()),
            author = u
        )
 
        db.session.add(p)
    db.session.commit()

def comments(count = 200):
    fake = Faker()
    user_count = User.query.count()
    post_count = Post.query.count()

    i=0
    while i<count:
        u = User.query.offset(randint(0,user_count-1)).first()
        p = Post.query.offset(randint(0,post_count-1)).first()

        if p.author_id != u.id:
            c = Comment(
                body = fake.text(),
                time_stamp = fake.date_time_between(p.time_stamp,datetime.utcnow()),
                author = u,
                post = p
            )
            i+=1
            db.session.add(c)
    db.session.commit()

def follows():
    user_count = User.query.count()
    users = User.query.all()
    for user in users:
        for i in range(user_count):
            following_user = users[i]
            user.follow(following_user)
            db.session.add(user)
    db.session.commit()

