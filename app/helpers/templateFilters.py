import datetime
from app import telomere

@telomere.template_filter('datetime_format')
def datetime_format(value):
    return value.strftime('%c')
