from multiprocessing import Value
import mariadb

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = mariadb.connect(
            user='admin',
            password='admin',
            host='127.0.0.1',
            port=3306,
            database='RFID'
        )
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def get_cursor():
    db = get_db()
    cur = db.cursor()
    return(cur)


def db_commit():
    db = get_db()
    db.commit()


def cursor_to_dict_array(cur):
    res = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    return res


def init_db():
    """Clear existing data and create new tables."""
    print('not functional!')
    #db = get_db()

    # with current_app.open_resource("schema.sql") as f:
    #     db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")
