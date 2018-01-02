from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired, Length


class LoginForm(Form):
    username = StringField(
        'username',
        validators=[InputRequired()]
    )
    cwid = StringField(
        'Campus Wide ID',
        validators=[InputRequired(), Length(min=8, max=8)]
    )
