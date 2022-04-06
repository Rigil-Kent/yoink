from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class DownloadForm(FlaskForm):
    url = StringField('Comic URL', validators=[DataRequired()])
    series = BooleanField('Series? ')
    download = SubmitField('Download')