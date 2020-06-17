from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User,Post
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
        print(u)
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
        print(p)
        db.session.add(p)
    db.session.commit()