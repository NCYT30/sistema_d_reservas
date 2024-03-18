from peewee import *
from datetime import datetime


database = MySQLDatabase('sistema_de_reservas',
                         user = 'root',
                         password = 'NCYT30',
                         host = 'localhost',
                         port = 3306)


class User(Model):
    
    name = CharField(max_length = 25)
    email = CharField(max_length = 35)
    password = CharField(max_length = 512)

    class Meta:
        database = database
        table_name = 'Users'


class Service(Model):

    name = CharField(max_length = 25)
    description = CharField(max_length = 100)
    price = IntegerField()
    availability = IntegerField()

    class Meta:
        database = database
        table_name = 'Service'


class Reservation(Model):

    user_id = ForeignKeyField(User, backref = 'users')
    service_id = ForeignKeyField(Service, backref = 'service')
    date_time = CharField(max_length = 15)
    status = IntegerField()

    class Meta: 
        database = database
        table_name = 'Reservation'


class Notification(Model):

    user_id = ForeignKeyField(User, backref = 'users')
    message = CharField(max_length = 50)
    sent_date = CharField(max_length = 15)

    class Meta:
        database = database
        table_name = 'Notification'