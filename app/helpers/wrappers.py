from functools import wraps
from flask import redirect, url_for
from app.model.manifest import Manifest

def manifest_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        manifest_count = Manifest.query.count()

        if manifest_count == 0:
            return redirect(url_for('manifest_upload'))

        return func(*args, **kwargs)

    return decorated_view

