import datetime
from peewee import *
from slugify import slugify
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('journal.db')

class Journal(Model):
    title = TextField(unique = True)
    date = DateField()
    time_spent = IntegerField()
    what_you_lean = TextField()
    resource_to_remember = TextField()
    tag = TextField()
    slug = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date')

    @classmethod
    def create_journal(cls,
        title, date, time_spent,
        what_you_lean, resource_to_remember, tag):
        try:
            with DATABASE.transaction():
                cls.create(
                    title = title,
                    date = date,
                    time_spent = time_spent,
                    what_you_lean = what_you_lean,
                    resource_to_remember = resource_to_remember,
                    tag = tag,
                    slug = slugify(title))
        except IntegrityError:
            raise ValueError("title already exists")

    def save(self,force_insert=False):
        try:
            super().save()
        except IntegrityError:
            raise ValueError("title already exists")





class User(UserMixin, Model):
    username = CharField(unique = True)
    password = CharField()

    @classmethod
    def create_user(cls, username, password):
        try:
            with DATABASE.transaction():
                cls.create(username = username, password = generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists")

    class Meta:
        database = DATABASE



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Journal, User], safe=True)
    DATABASE.close()
