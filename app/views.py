from pony.orm import select
from app import app
from app.models import db, Task
from pony.orm.examples.estore import *

from flask import render_template


@app.route("/")
def view():
    query = Task.select().order_by(Task.id)
    return render_template('view.html', query=query)


