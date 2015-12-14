from flask_wtf import Form
from wtforms import StringField, BooleanField, SelectField, HiddenField, FormField, DecimalField, IntegerField, Form as WtfForm
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms.fields.html5 import DateTimeField
from wtforms_components import read_only

class BatchForm(WtfForm):
    robot = StringField('Robot', validators=[DataRequired(), Length(max=20)])
    temperature = DecimalField('Temperature', validators=[DataRequired()], places=1)
    datetime = DateTimeField('Date and Time', validators=[DataRequired()], format='%d/%m/%Y %H:%M')
    plateName = StringField('Plate Name', validators=[DataRequired(), Length(max=50)])
    halfPlate = SelectField('Half Plate', choices=[(None, ''), ('A', 'A'), ('B', 'B')])
    humidity = IntegerField('Humidity', validators=[DataRequired(), NumberRange(min=20, max=65)])
    primerBatch = IntegerField('Primer Batch', validators=[DataRequired(), NumberRange(min=1, max=20)])
    enzymeBatch = IntegerField('Enzyme Batch', validators=[DataRequired(), NumberRange(min=1, max=20)])
    rotorGene = IntegerField('Rotor Gene', validators=[DataRequired(), NumberRange(min=1, max=8)])
    operatorUserId = SelectField('Operator', coerce=int)
    failed = BooleanField('Failed')

class BatchEditForm(Form):
    id = HiddenField('id')
    version_id = HiddenField('version_id')
    batch = FormField(BatchForm)

    def __init__(self, *args, **kwargs):
        super(BatchEditForm, self).__init__(*args, **kwargs)
        read_only(self.batch.failed)

class BatchDelete(Form):
    id = HiddenField('id')
