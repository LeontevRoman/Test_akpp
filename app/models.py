
from datetime import date
from pony.orm import Database, Required, PrimaryKey, Optional


db = Database()

class Task(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    description = Optional(str)
    date = Required(date)
    flag = Required(bool)

    def __str__(self):
        return f'{self.name}, {self.description}'
        
