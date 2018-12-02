from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('novel', __name__)


@bp.route('/')
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM novel.post p JOIN novel.user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    posts = cur.fetchall()
    return render_template('novel/index.html', posts=posts)


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    cur = get_db().cursor()
    cur.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM novel.post p JOIN novel.user u ON p.author_id = u.id'
        ' WHERE p.id = %s',id )

    post = cur.fetchone()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        db = get_db()
        cur = db.cursor()

        cur.execute('SELECT title FROM novel.post WHERE title = %s', title)
        newTitle = cur.fetchone()

        if not title:
            error = 'Title is required.'

        if newTitle and newTitle['title'] == title:
            error = 'Title is repeated.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.cursor().execute(
                'INSERT INTO novel.post (title, body, author_id) VALUES ("{0}", "{1}", "{2}")'
                .format(title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('novel.index'))

    return render_template('novel/create.html')


@bp.route('/<int:NoteId>/detail')
def detail(NoteId):

    db = get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT title, body FROM novel.post where id = %s',NoteId
    )
    content = cur.fetchone()

    return render_template('novel/detail.html',detail=content)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        cur.execute('SELECT id FROM novel.post WHERE title = %s', title)
        newId = cur.fetchone()



        if not title:
            error = 'Title is required.'

        if newId and newId['id'] != id:
            error = 'Title is repeated.'

        if error is not None:
            flash(error)
        else:

            cur.execute(
                'UPDATE novel.post SET title = "{0}", body = "{1}" WHERE id = {2}'
                .format(title, body, id)
            )
            db.commit()
            return redirect(url_for('novel.index'))

    return render_template('novel/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.cursor().execute('DELETE FROM novel.post WHERE id = %s', id)
    db.commit()
    return redirect(url_for('novel.index'))


@bp.route('/search',methods=('POST','GET'))
def search():
    if request.method == 'POST':
        title = request.form['title']
        db = get_db()
        cur = db.cursor()
        cur.execute(
            'select * from novel.post where title like "%{0}%"'.format(title)
        )

        notes = cur.fetchall()
        return render_template('novel/searchRes.html',notes= notes)
    return render_template('novel/search.html')




