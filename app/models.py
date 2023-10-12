
from datetime import date
from flask_login import UserMixin
from pony.orm import Database, Required, PrimaryKey, Optional


db = Database()


class Task(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    description = Optional(str)
    date = Required(date)
    flag = Required(bool)

    def __str__(self):
        return f'{self.id}, {self.name}, {self.description}'


class User(db.Entity, UserMixin):
    login = Required(str, unique=True)
    password = Required(str)
    last_login = Optional(date)