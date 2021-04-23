from peewee import *
from config import *


class DbConnection():

    dbhandle = MySQLDatabase(
        name_db, user=user_db,
        password=password_db,
        host=host_db, 
        charset='utf8'
    )

