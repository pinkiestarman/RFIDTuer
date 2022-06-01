from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import cursor_to_dict_array, get_cursor, get_db

bp = Blueprint("admin", __name__)


@bp.route("/")
@login_required
def index():
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
        " ORDER BY g.id ASC"
    )
    gruppen = cursor_to_dict_array(cur)

    cur.execute(
        "SELECT l.id, l.name"
        " FROM  location l"
        " ORDER BY l.id ASC"
    )
    locations = cursor_to_dict_array(cur)

    cur.close()

    if (g.user is None):
        abort(403)

    if(g.user["admin_flag"] == 1):
        return render_template("admin/index.html", gruppen=gruppen, users=users, locations=locations)
    else:
        abort(403)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (
                    title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
