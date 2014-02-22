import os
import os.path as op
from operator import itemgetter

from flask import url_for, redirect, request, flash
from flask.ext import admin, login
from flask.ext.admin import expose
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.babel import gettext
from flask.ext.admin._compat import urljoin
from flask.ext.login import UserMixin
from wtforms import fields, validators
from wtforms.form import Form

from app import app

path = op.dirname(__file__)
static = op.join(path, 'static')


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
    allowed_extensions = None
    editable_extensions = ('md')

    list_template = 'admin/page_list.html'
    edit_template = 'admin/page_edit.html'

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('admin.index'))
        else:
            return super(PageAdmin, self).index()

    def on_edit_file(self, full_path, path):
        """Prepends a new line after edit, otherwise FlatPages' YAML doesn't
        render it.
        """
        with open(full_path, 'r+b') as f:
            data = f.read()
            f.seek(0)
            f.write('\n'+data)
            f.truncate()
        return super(PageAdmin, self).on_edit_file(full_path, path)

    def _get_file_url(self, path):
        """Overriding private method to modify '*.md' urls to their respective
        markdown-rendered pages.

        Original source in flask_admin/contrib/fileadmin.py
        """
        if self.is_file_editable(path):
            if path[-3:] == '.md':
                # Truncate '.md' extension from url.
                return url_for(".edit", path='%s/' % path[:-3])
            else:
                return url_for(".edit", path=path)
        else:
            base_url = self.get_base_url()
            if path[-3:] == '.md':
                # Like above.
                return urljoin(base_url, '%s/' % path[:-3])
            else:
                return urljoin(base_url, path)


class UploadAdmin(FileAdmin):
    """Other file upload/edit (images, videos, etc.)"""
    list_template = 'admin/upload_list.html'

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('admin.index'))
        else:
            return super(UploadAdmin, self).index()

    @app.context_processor
    def my_processor():
        """Custom template function to determine if file is an image or not.
        Used to generate thumbnails in 'File' admin.
        """
        def is_image(img):
            if op.splitext(img)[1] in ['.'+e for e in ['jpg', 'jpeg', 'png', 'gif', 'bmp']]:
                return True
            else:
                return False
        return dict(is_image=is_image)


init_login()

admin = admin.Admin(app, 'Admin', index_view=MyAdminIndexView(name='Login'), base_template='admin/master.html')

admin.add_view(PageAdmin(op.join(path, 'pages'), base_url='/', name='Pages', endpoint='pages'))
admin.add_view(UploadAdmin(op.join(static, 'uploads'), base_url='/static/uploads/', name='Files', endpoint='files'))
