from peewee import *
import datetime
from db import DbConnection


class BaseModel(Model):
    class Meta:
        database = DbConnection.dbhandle


class News(BaseModel):

    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
    text = CharField()

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())
        
    class Meta:
        table_settings = ['DEFAULT CHARSET=utf8']
