from datetime import timedelta

from flask import render_template, request, session
from wtforms import Form
from wtforms.csrf.session import SessionCSRF


class BaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF

        @property
        def csrf_context(self):
            return session


class DeleteForm(BaseForm):
    pass


class Formist:
    def __init__(self, app=None):
        self.BaseForm = BaseForm
        self.DeleteForm = DeleteForm

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.BaseForm.Meta.csrf_secret = app.config.get("CSRF_SECRET_KEY")
        self.BaseForm.Meta.csrf_time_limit = timedelta(
            minutes=app.config.get("CSRF_TIME_LIMIT", 30)
        )

    @staticmethod
    def handle_form(*, form_cls, template, on_success, cancel_url, obj=None):
        if request.method == "GET":
            form = form_cls(obj=obj)
        else:  # POST
            form = form_cls(formdata=request.form)
            if form.validate():
                return on_success(form)

        return render_template(template, form=form, obj=obj, cancel_url=cancel_url)
