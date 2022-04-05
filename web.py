import os
import threading
from flask import Flask, render_template, url_for, request, flash, make_response, redirect, send_from_directory
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

from yoink.config import config
from yoink.comic import Comic


class DownloadForm(FlaskForm):
    url = StringField('Comic URL', validators=[DataRequired()])
    series = BooleanField('Series? ')
    download = SubmitField('Download')

app = Flask(__name__)
moment = Moment(app)
app.config['SECRET_KEY'] = 'snapekilleddumpledork'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(config.app_root, "data.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name!r}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self): return f'<User {self.username!r}>'

class ComicMeta(db.Model):
    __tablename__ = 'comicmeta'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True, index=True)
    issue = db.Column(db.Integer, nullable=True, index=True)
    category = db.Column(db.String(128), index=True, nullable=True)
    previous_issue = db.Column(db.String(256), nullable=True)
    next_issue = db.Column(db.String(256), nullable=True)
    cover_path = db.Column(db.String(256))
    archive_path = db.Column(db.String(256))


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(os.path.join(config.library_path, 'comics'), filename, as_attachment=True)


def get_cover_path(comic):
    return [image for image in os.listdir(os.path.join(config.library_path, 'comics', comic.title)) if image.endswith('000.jpg')][0]


def get_archive_path(comic):
    return [image for image in os.listdir(os.path.join(config.library_path, 'comics', comic.title)) if image.endswith('.cbr')][0]
    

def get_comic_library_meta():
    comic_meta = []

    for comic in ComicMeta.query.all():
        comic_meta.append({
            'cover': comic.cover_path,
            'title': comic.title,
            'archive': comic.archive_path
        })

    return comic_meta


@app.route('/', methods=['post','get'])
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

        comic.archiver.download()
        comic.archiver.generate_archive()


        if comic_meta is None:
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

            return render_template('index.html', form=form, url=url, series=series, latest=latest), 200


        if form.series.data:
            print('Download the whole damn lot')

        flash(f'{comic.title} downloaded to {os.path.join(config.library_path, "comics/" + comic.title)}')

        latest = get_comic_library_meta()
        comic.archiver.cleanup_worktree()
        form.url.data = ''

    return render_template('index.html', form=form, url=url, series=series, latest=latest), 200
    