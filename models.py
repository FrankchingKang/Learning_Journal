import datetime
from peewee import *

DATABASE = SqliteDatabase('journal.db')

class Journal(Model):
    title = TextField()
    date = DateField()
    time_spent = IntegerField()
    what_you_lean = TextField()
    resource_to_remember = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date')

    @classmethod
    def create_journal(cls,
        title, date, time_spent,
        what_you_lean, resource_to_remember):
        with DATABASE.transaction():
            cls.create(
                title = title,
                date = date,
                time_spent = time_spent,
                what_you_lean = what_you_lean,
                resource_to_remember = resource_to_remember)



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Journal], safe=True)
    DATABASE.close()
