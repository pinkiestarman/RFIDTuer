from crypt import methods
from urllib.error import HTTPError
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('rfid', __name__)


@bp.route('/user/create', methods=['POST'])
@login_required
def user_create():
    if 'user-name' in request.form and 'user-TransponderID' in request.form:
        username = request.form['user-name']
        transponderID = request.form['user-TransponderID']
        db = get_db()
        db.execute(
            'INSERT INTO user (Name, TransponderID, Passwort_hash) VALUES (?, ?, ?)',
            (username, transponderID,
             'pbkdf2:sha256:260000$ClAB2AQV4Jzr8zv8$61cd04ff86bb8a46a7e1fc5caa40ab5be15aca8407227693f50c730cd87c1254',),
        )
        db.commit()
    return redirect(url_for('admin.index'))


@bp.route('/location/create', methods=['POST'])
@login_required
def location_create():
    if 'location-name' in request.form:
        location = request.form['location-name']
        db = get_db()
        db.execute('INSERT INTO Location (Name) VALUES (?)', (location,))
        db.commit()
    return redirect(url_for('admin.index'))


@bp.route('/gruppe/create', methods=['POST'])
@login_required
def gruppe_create():
    if 'gruppe-name' in request.form:
        gruppe = request.form['gruppe-name']
        db = get_db()
        if(db.execute('SELECT Name FROM Location WHERE Name=?', (gruppe,)).fetchone() == None):
            db.execute(
                'INSERT OR IGNORE INTO Gruppe (Name) VALUES (?)', (gruppe,))
            db.commit()
        else:
            flash("Name der Gruppe existiert bereits")
    return redirect(url_for('admin.index'))
