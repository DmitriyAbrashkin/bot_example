import peewee
from models import *
from db import DbConnection


def add_news(name, text):
    row = News(
        name=name,
        text=text
    )
    row.save()



""" if __name__ == '__main__':
    try:
        News.create_table()
    except peewee.InternalError as px:
        print(str(px)) """

add_news("I born", "Smth staff")
add_news("Study", "Smth staff")
