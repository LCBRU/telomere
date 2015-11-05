from flask_wtf import Form
from wtforms import StringField, HiddenField, FormField, DecimalField, Form as WtfForm
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateTimeField

class BatchForm(WtfForm):
    batchCode = StringField('Batch Code', validators=[DataRequired(), Length(max=20)])
    robot = StringField('Robot', validators=[DataRequired(), Length(max=20)])
    pcrMachine = StringField('PCR Machine', validators=[DataRequired(), Length(max=20)])
    temperature = DecimalField('Temperature', validators=[DataRequired()], places=1)
    datetime = DateTimeField('Date and Time', validators=[DataRequired()], format='%d/%m/%Y %H:%M')

class BatchEditForm(Form):
    id = HiddenField('id')
    version_id = HiddenField('version_id')
    batch = FormField(BatchForm)

class BatchDelete(Form):
    id = HiddenField('id')

