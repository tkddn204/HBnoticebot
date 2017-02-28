# db models
import datetime

from db import *


class BaseModel(Model):
    class Meta:
        database = db


class Notices(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True)
    num = IntegerField(default=0)
    datetime = DateTimeField(default=datetime.datetime.now())


class Users(BaseModel):
    user_id = IntegerField(unique=True)
    is_set = BooleanField(default=False)
