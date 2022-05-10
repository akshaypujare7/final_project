import os.path

import click
from flask.cli import with_appcontext
from app.db import db


@click.command(name='create-db')
@with_appcontext
def create_database():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(file_dir, "../../database")
    print(db_dir)

    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    db.create_all()
