from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.SQL.db import cursor_to_dict_array, get_cursor, db_commit

bp = Blueprint("admin", __name__)


@bp.route("/")
@login_required
def index():

    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    """Show all the posts, most recent first."""
    cur = get_cursor()
    cur.execute(
        "SELECT u.id, u.name, u.transponder_id"
        " FROM  user u"
        " ORDER BY u.id ASC"
    )
    users = cursor_to_dict_array(cur)

    cur.execute(
        "SELECT g.id, g.name"
        " FROM  gruppe g"
        " WHERE g.user_id IS NULL"
        " ORDER BY g.id ASC"
    )
    gruppen = cursor_to_dict_array(cur)

    cur.execute(
        "SELECT l.id, l.name"
        " FROM  location l"
        " ORDER BY l.id ASC"
    )
    locations = cursor_to_dict_array(cur)

    cur.execute(
        "SELECT recht.id, location.name as location_name from recht JOIN location ON recht.objekt_id=location.id ORDER BY recht.id ASC"
    )
    rechte = cursor_to_dict_array(cur)
    print(rechte)
    cur.close()

    return render_template("admin/index.html", gruppen=gruppen, users=users, locations=locations, rechte=rechte)

# Actions for Table 'ort'


@bp.route("/location", methods=("GET",))
@login_required
def location():
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    cur = get_cursor()
    cur.execute(
        "WITH RECURSIVE cte as ("
        " SELECT id, name, parent_id, client_id, 0 as Level, name as fancy_name, name as sort"
        " FROM location"
        " WHERE parent_id IS NULL"
        " UNION ALL"
        " SELECT l.id, l.name, l.parent_id, l.client_id, Level + 1 as Level, Concat(REPEAT('____', Level + 1),l.name) as fancy_name, Concat(sort,' : ',l.name) as sort"
        " FROM location l"
        " INNER JOIN cte"
        " ON l.parent_id=cte.id"
        ")"
        " SELECT * FROM cte"
        " ORDER BY sort"
    )
    locations = cursor_to_dict_array(cur)
    print(locations)
    cur.close()

    return render_template("admin/location.html", locations=locations)


@bp.route('/location/create', methods=['POST'])
@login_required
def location_create():
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    if 'location-name' in request.form:
        location = request.form['location-name']
        cur = get_cursor()
        cur.execute('INSERT INTO location (name) VALUES (?)', (location,))
        db_commit()
    return redirect(url_for('admin.location'))


@bp.route('/location/<int:id>/delete', methods=['GET'])
@login_required
def location_delete(id):
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    cur = get_cursor()
    cur.execute('DELETE FROM location WHERE id=?', (id,))
    db_commit()
    return redirect(url_for('admin.location'))


@bp.route('/location/<int:id>', methods=['GET'])
@login_required
def location_view(id):
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    cur = get_cursor()
    cur.execute('SELECT * FROM location WHERE id=?', (id,))
    location = cursor_to_dict_array(cur)
    db_commit()
    return render_template('/admin/location_view.html', location=location[0])

# Actions for Table 'gruppe'


@bp.route("/gruppe", methods=("GET",))
@login_required
def gruppe():
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    cur = get_cursor()
    cur.execute(
        "SELECT g.id, g.name, g.user_id"
        " FROM  gruppe g"
        " ORDER BY g.id ASC"
    )
    gruppen = cursor_to_dict_array(cur)
    cur.close()

    return render_template("admin/gruppe.html", gruppen=gruppen)


@bp.route('/gruppe/create', methods=['POST'])
@login_required
def gruppe_create():
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)
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
    return redirect(url_for('admin.gruppe'))


@bp.route("/gruppe/<int:id>/delete", methods=("POST", "GET",))
@login_required
def gruppe_delete(id):
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    cur = get_cursor()
    cur.execute('DELETE FROM gruppe WHERE id = ?', (id,))
    db_commit()
    return redirect(url_for('admin.gruppe'))


@bp.route("/gruppe/<int:id>", methods=("GET",))
@login_required
def gruppe_view(id):
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    cur = get_cursor()
    cur.execute(
        "SELECT g.id, g.name, g.user_id"
        " FROM  gruppe g"
        " WHERE g.id=?", (id,)
    )
    gruppe = cursor_to_dict_array(cur)

    cur.execute(
        "SELECT user.id, user.name"
        " FROM gruppe"
        " INNER JOIN user_gruppe"
        " ON gruppe.id=user_gruppe.gruppe_id"
        " INNER JOIN user"
        " ON user_gruppe.user_id=user.id"
        " WHERE gruppe.id=?", (id,)
    )
    users = cursor_to_dict_array(cur)
    print(users)
    cur.execute(
        " SELECT location.id, location.name"
        " FROM user"
        " INNER JOIN user_gruppe"
        " ON user.id=user_gruppe.user_id"
        " INNER JOIN gruppe"
        " ON user_gruppe.gruppe_id=gruppe.id"
        " INNER JOIN gruppe_recht"
        " ON gruppe.id=gruppe_recht.gruppe_id"
        " INNER JOIN recht"
        " ON gruppe_recht.recht_id=recht.id"
        " INNER JOIN location"
        " ON recht.objekt_id=location.id"
        " WHERE gruppe.id=?", (id,)
    )

    locations = cursor_to_dict_array(cur)
    cur.close()

    return render_template("admin/gruppe_view.html", gruppe=gruppe[0], users=users, locations=locations)

# Actions for Table 'user'


@bp.route("/user", methods=("GET",))
@login_required
def user():
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    cur = get_cursor()
    cur.execute(
        "SELECT u.id, u.name, u.transponder_id"
        " FROM  user u"
        " ORDER BY u.id ASC"
    )
    users = cursor_to_dict_array(cur)
    cur.close()

    return render_template("admin/user.html", users=users)


@bp.route("/user/<int:id>", methods=("GET",))
@login_required
def user_view(id):
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    cur = get_cursor()
    cur.execute(
        "SELECT u.id, u.name, u.transponder_id"
        " FROM  user u"
        " WHERE u.id=?", (id,)
    )
    user = cursor_to_dict_array(cur)

    cur.execute(
        "SELECT gruppe.id, gruppe.name, gruppe.user_id"
        " FROM user"
        " INNER JOIN user_gruppe"
        " ON user.id=user_gruppe.user_id"
        " INNER JOIN gruppe"
        " ON user_gruppe.gruppe_id=gruppe.id"
        " WHERE user.id=?", (id,)
    )
    gruppen = cursor_to_dict_array(cur)

    cur.execute(
        " SELECT location.id, location.name"
        " FROM user"
        " INNER JOIN user_gruppe"
        " ON user.id=user_gruppe.user_id"
        " INNER JOIN gruppe"
        " ON user_gruppe.gruppe_id=gruppe.id"
        " INNER JOIN gruppe_recht"
        " ON gruppe.id=gruppe_recht.gruppe_id"
        " INNER JOIN recht"
        " ON gruppe_recht.recht_id=recht.id"
        " INNER JOIN location"
        " ON recht.objekt_id=location.id"
        " WHERE user.id=?", (id,)
    )

    locations = cursor_to_dict_array(cur)
    print(locations)
    cur.close()

    return render_template("admin/user_view.html", user=user[0], gruppen=gruppen, locations=locations)


@bp.route("/user/<int:id>/delete", methods=("POST", "GET",))
@login_required
def user_delete(id):
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    cur = get_cursor()
    cur.execute('DELETE FROM user WHERE id = ?', (id,))
    db_commit()
    return redirect(url_for('admin.user'))


@bp.route("/user/create", methods=("POST",))
@login_required
def user_create():
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

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
    return redirect(url_for('admin.user'))


@bp.route("/user/update", methods=("POST",))
@login_required
def user_update(id):
    if (g.user is None):
        abort(403)

    if(g.user['admin_flag'] != 1):
        return abort(403)

    cur = get_cursor()

    return redirect(url_for('admin.index'))
