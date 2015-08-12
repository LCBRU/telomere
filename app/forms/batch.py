from flask_wtf import Form
from wtforms import StringField, FieldList, FormField, DecimalField, Form as WtfForm
from wtforms.validators import DataRequired, ValidationError, StopValidation, Length
from wtforms_components import TimeField, read_only
from wtforms.fields.html5 import DateTimeField

class RequiredIfSampleCode(object):
    def __call__(self, form, field):
    	if (not form.sampleCode.data):
	        field.errors[:] = []
	        # Stop further validators running
	        raise StopValidation()

class RequiredIfSampleDataEntered(object):
    def __init__(self, message=None):
        if not message:
            message = u'Sample Code Required if other data has been entered'
        self.message = message

    def __call__(self, form, field):
    	if (not field.data and (form.t1.data or form.s1.data or form.t2.data or form.s2.data or form.tsRatio.data)):
            raise ValidationError(self.message)

class SampleForm(WtfForm):
    sampleCode = StringField('Sample Code', validators=[RequiredIfSampleDataEntered()])
    t1 = DecimalField('T1', validators=[RequiredIfSampleCode()], places=1)
    s1 = DecimalField('S1', validators=[RequiredIfSampleCode()], places=1)
    t2 = DecimalField('T2', validators=[RequiredIfSampleCode()], places=1)
    s2 = DecimalField('S2', validators=[RequiredIfSampleCode()], places=1)
    tsRatio = DecimalField('T/S', validators=[RequiredIfSampleCode()], places=1)

class BatchForm(WtfForm):
    batchCode = StringField('Batch Code', validators=[DataRequired(), Length(max=20)])
    operator = StringField('Operator')
    robot = StringField('Robot', validators=[DataRequired(), Length(max=20)])
    pcrMachine = StringField('PCR Machine', validators=[DataRequired(), Length(max=20)])
    temperature = DecimalField('Temperature', validators=[DataRequired()], places=1)
    datetime = DateTimeField('Date and Time', validators=[DataRequired()], format='%d/%m/%Y %H:%M')

    def __init__(self, *args, **kwargs):
        super(BatchForm, self).__init__(*args, **kwargs)
        read_only(self.operator)

class BatchAndSampleForm(Form):
    batch = FormField(BatchForm)
    samples = FieldList(FormField(SampleForm), min_entries=48)

