import os.path as op

from flask import url_for, redirect, request
from flask.ext import admin, login
from flask.ext.admin import expose
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.login import UserMixin
from wtforms import fields, validators
from wtforms.form import Form

from app import app, static


class MyUser(UserMixin):
    id = 'admin'


# TODO Save password properly, not in plaintext!
password = 'admin'
class LoginForm(Form):
    """Define login and registration forms (for flask-login)."""
    def validate_login(self, field):
        print self.password.data
        if self.password.data != password:
            raise validators.ValidationError('Invalid password')

    password = fields.PasswordField(validators=[validators.required(),
                                                validate_login])


def init_login():
    """Initialize flask-login."""
    login_manager = login.LoginManager()
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return MyUser()


class MyAdminIndexView(admin.AdminIndexView):
    """Create customized index view class."""

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        else:
            return self.render('admin/index.html')

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            login.login_user(MyUser())

        if login.current_user.is_authenticated():
            return redirect(url_for('pages.index'))

        # self._template_args['form'] = form
        return self.render('admin/login.html', form=form)

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class PageAdmin(FileAdmin):
    """Page edit."""
    can_upload = False
    can_delete = False
    can_delete_dirs = False
    can_mkdir = False
    can_rename = False
    allowed_extensions = editable_extensions = ('jpg', 'jpeg', 'png', 'gif', 'tif', 'tiff', 'bmp')

    list_template = 'admin/page_list.html'

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('admin.index'))
        else:
            return super(PageAdmin, self).index()


class UploadAdmin(FileAdmin):
    """Other file upload/edit (images, videos, etc.)"""
    list_template = 'admin/upload_list.html'

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('admin.index'))
        else:
            return super(UploadAdmin, self).index()


init_login()

admin = admin.Admin(app, 'Admin', index_view=MyAdminIndexView(name='Login'))

admin.add_view(PageAdmin(op.join(static, 'pages'), '/static/pages/', name='Pages', endpoint='pages'))
admin.add_view(UploadAdmin(op.join(static, 'uploads'), '/static/uploads/', name='Files', endpoint='files'))
