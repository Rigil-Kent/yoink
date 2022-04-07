import os
from datetime import datetime

from flask import render_template, session, send_from_directory, redirect, url_for, flash, g

from app.main import main
from app.main.forms import DownloadForm
from app import db
from app.email import send_email
from app.models import User, Role, ComicMeta
from yoink.comic import Comic
from yoink.config import config


@main.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(os.path.join(config.library_path, 'comics'), filename, as_attachment=True)


def get_cover_path(comic):
    return [image for image in os.listdir(os.path.join(config.library_path, 'comics', comic.title)) if image.endswith('000.jpg')][0]


def get_archive_path(comic):
    return [image for image in os.listdir(os.path.join(config.library_path, 'comics', comic.title)) if image.endswith('.cbr')][0]
    

def get_comic_library_meta():
    comic_meta = []

    for comic in ComicMeta.query.order_by(ComicMeta.id.desc()).all():
        comic_meta.append({
            'cover': comic.cover_path,
            'title': comic.title,
            'archive': comic.archive_path
        })

    return comic_meta


def new_user(username, db, app, form):
    user = User.query.filter_by(username=username).first()

    if user is None:
        user = User(username=form.username.data, role_id=3)
        db.session.add(user)
        if app.config['YOINK_ADMIN']:
            send_email(app.config['YOINK_ADMIN'], 'New User', 'mail/new_user', user=user)
        db.session.commit()


def check_setup():
    if User.query.all() is None:
        return redirect(url_for('setup'))


@main.route('/', methods=['post', 'get'])
def index():
    url = None
    series = False
    form = DownloadForm()
    latest = get_comic_library_meta()

    if form.validate_on_submit():
        url = form.url.data.strip()
        series = form.series.data

        comic = Comic(url)
        comic_meta = ComicMeta.query.filter_by(title=comic.title).first()

        if comic_meta is None:
            comic.archiver.download()
            comic.archiver.generate_archive()

            comic_meta = ComicMeta()
            comic_meta.title = comic.title
            comic_meta.category = comic.category
            comic_meta.issue = comic.issue_number
            comic_meta.next_issue = comic.next
            comic_meta.previous_issue = comic.prev
            comic_meta.cover_path = os.path.join(comic.title, get_cover_path(comic))
            comic_meta.archive_path = os.path.join(comic.title, get_archive_path(comic))

            db.session.add(comic_meta)
            db.session.commit()
        else:
            flash(f'Comic {comic.title} exists')

            latest = get_comic_library_meta()
            form.url.data = ''

            return render_template('index.html', form=form, url=url, series=series, latest=latest, status=g.status_code), 200


        if form.series.data:
            print('Download the whole damn lot')

        flash(f'{comic.title} downloaded to {os.path.join(config.library_path, "comics/" + comic.title)}')

        latest = get_comic_library_meta()
        comic.archiver.cleanup_worktree()
        form.url.data = ''

    return render_template('index.html', form=form, url=url, series=series, latest=latest), 200