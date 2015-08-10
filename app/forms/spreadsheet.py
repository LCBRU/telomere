from flask_wtf import Form
from flask_wtf.file import FileField as _FileField, FileAllowed, FileRequired
from wtforms.widgets import FileInput as _FileInput

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
    spreadsheet = FileField('Spreadsheet', accept=['application/vnd.ms-excel'], validators=[
        FileRequired(),
        FileAllowed(['xls'], 'Only XLS spreadsheets allowed')
    ])
