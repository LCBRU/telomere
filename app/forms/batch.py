from flask_wtf import Form
from wtforms import StringField, SelectField, HiddenField, FormField, DecimalField, Form as WtfForm
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateTimeField

class BatchForm(WtfForm):
    batchCode = StringField('Batch Code', validators=[DataRequired(), Length(max=20)])
    robot = StringField('Robot', validators=[DataRequired(), Length(max=20)])
    pcrMachine = StringField('PCR Machine', validators=[DataRequired(), Length(max=20)])
    temperature = DecimalField('Temperature', validators=[DataRequired()], places=1)
    datetime = DateTimeField('Date and Time', validators=[DataRequired()], format='%d/%m/%Y %H:%M')
    plateName = StringField('Plate Name', validators=[DataRequired(), Length(max=50)])
    halfPlate = SelectField('Half Plate', choices=[(None, ''), ('A', 'A'), ('B', 'B')])
    humidity = DecimalField('Humidity', validators=[DataRequired()], places=2)
    primerBatch = StringField('Primer Batch', validators=[DataRequired(), Length(max=50)])
    enzymeBatch = StringField('Enzyme Batch', validators=[DataRequired(), Length(max=50)])
    rotorGene = StringField('Rotor Gene', validators=[DataRequired(), Length(max=50)])

class BatchEditForm(Form):
    id = HiddenField('id')
    version_id = HiddenField('version_id')
    batch = FormField(BatchForm)

class BatchDelete(Form):
    id = HiddenField('id')

class BatchCompleteAllErrors(Form):
    id = HiddenField('id')

class BatchCompleteError(Form):
    batchId = HiddenField('batchId')
    id = HiddenField('id')
    page = HiddenField('page')

