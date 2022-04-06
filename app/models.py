from app import db


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