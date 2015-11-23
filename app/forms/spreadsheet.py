from flask_wtf import Form
from wtforms import FormField
from flask_wtf.file import FileField as _FileField, FileAllowed, FileRequired
from wtforms.validators import ValidationError
from wtforms.widgets import FileInput as _FileInput
from app.forms.batch import BatchForm

class RequiredIfBatchNotFailed(object):
    def __init__(self, message=None):
        if not message:
            message = u'Spreadsheet is required'
        self.message = message

    def __call__(self, form, field):
        if (not form.batch.failed.data and not form.spreadsheet.data):
            raise ValidationError(self.message)

class FileInput(_FileInput):

    def __call__(self, field, **kwargs):
        if field.accept:
            kwargs[u'accept'] = ','.join(field.accept)
        return _FileInput.__call__(self, field, **kwargs)


class FileField(_FileField):
    widget = FileInput()

    def __init__(self, *args, **kwargs):
        self.accept = kwargs.pop('accept', None)
        super(FileField, self).__init__(*args, **kwargs)

class SpreadsheetUpload(Form):
    batch = FormField(BatchForm)
    spreadsheet = FileField('Spreadsheet', accept=['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'], validators=[
        RequiredIfBatchNotFailed()
#        , FileAllowed(['.xlsx'], 'Only XLSX spreadsheets allowed')
    ])
