from quart_wtf import QuartForm
from wtforms.fields import (IntegerField, StringField, TextAreaField,
    HiddenField, SelectField)
from wtforms import validators


class DeviceForm(QuartForm):
    id = HiddenField('id', validators=[validators.optional()])
    interface = HiddenField('interface', validators=[validators.optional()])
    remove = HiddenField('remove', validators=[validators.optional()])
    name = StringField('name', validators=[validators.DataRequired()])
    room_id = SelectField('room')
    secret = StringField('secret', validators=[validators.optional()])
