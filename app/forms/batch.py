from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms_components import TimeField, read_only

class BatchEntry(Form):
    batchId = StringField('Batch Id', validators=[DataRequired()])
    operator = StringField('Operator')
    robot = StringField('Robot', validators=[DataRequired()])


    def __init__(self, *args, **kwargs):
        super(BatchEntry, self).__init__(*args, **kwargs)
        read_only(self.operator)
