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
from flaskr.db import db_commit, get_cursor, get_db

bp = Blueprint('rfid', __name__)


@bp.route('/user/create', methods=['POST'])
@login_required
def user_create():
    if 'user-name' in request.form and 'user-TransponderID' in request.form:
        username = request.form['user-name']
        transponderID = request.form['user-TransponderID']
        cur = get_cursor()
        cur.execute(
            'INSERT INTO user (name, transponder_id, passwort_hash) VALUES (?, ?, ?)',
            (username, transponderID,
             'pbkdf2:sha256:260000$ClAB2AQV4Jzr8zv8$61cd04ff86bb8a46a7e1fc5caa40ab5be15aca8407227693f50c730cd87c1254',),
        )
        db_commit()
    return redirect(url_for('admin.index'))


@bp.route('/location/create', methods=['POST'])
@login_required
def location_create():
    if 'location-name' in request.form:
        location = request.form['location-name']
        cur = get_cursor()
        cur.execute('INSERT INTO location (name) VALUES (?)', (location,))
        db_commit()
    return redirect(url_for('admin.index'))


@bp.route('/gruppe/create', methods=['POST'])
@login_required
def gruppe_create():
    if 'gruppe-name' in request.form:
        gruppe = request.form['gruppe-name']
        cur = get_cursor()
        cur.execute('SELECT name FROM location WHERE name=?', (gruppe,))
        if(cur.fetchone() == None):
            cur.execute(
                'INSERT INTO gruppe (name) VALUES (?)', (gruppe,))
            db_commit()
        else:
            flash("Name der Gruppe existiert bereits")
    return redirect(url_for('admin.index'))
