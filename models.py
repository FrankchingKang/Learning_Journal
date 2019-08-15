import datetime
from peewee import *
from slugify import slugify
from flask_login import UserMixin

DATABASE = SqliteDatabase('journal.db')

class Journal(Model):
    title = TextField()
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
        with DATABASE.transaction():
            cls.create(
                title = title,
                date = date,
                time_spent = time_spent,
                what_you_lean = what_you_lean,
                resource_to_remember = resource_to_remember,
                tag = tag,
                slug = slugify(title))




class User(UserMixin, Model):
    username = CharField(unique = True)
    password = CharField()

    class Meta:
        database = DATABASE



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Journal, User], safe=True)
    DATABASE.close()
