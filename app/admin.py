from flask import url_for, redirect, request
from flask.ext import admin, login
from flask.ext.admin import expose
from flask.ext.admin.contrib.mongoengine import ModelView
from wtforms import form, fields, validators
from jinja2 import Markup

from app import app, db, models


class User(db.Document):
    """Create user model. For simplicity, it will store passwords in plain
    text. Obviously that's not right thing to do in real world application.
    """
    login = db.StringField(max_length=80, unique=True)
    password = db.StringField(max_length=64)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    # Required for administrative interface
    def __unicode__(self):
        return self.login


class LoginForm(form.Form):
    """Define login and registration forms (for flask-login)."""
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.objects(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if User.objects(login=self.login.data):
            raise validators.ValidationError('Duplicate username')


def init_login():
    """Initialize flask-login."""
    login_manager = login.LoginManager()
    login_manager.setup_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=user_id).first()


class MyModelView(ModelView):
    """Create customized model view class."""
    def is_accessible(self):
        return login.current_user.is_authenticated()


class MyAdminIndexView(admin.AdminIndexView):
    """Create customized index view class."""

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))

        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link

        return self.render('admin/form.html')

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            user = User()

            form.populate_obj(user)
            user.save()

            login.login_user(user)
            return redirect(url_for('.index'))

        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link

        return self.render('admin/form.html')

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class ImageView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.path)))

    column_formatters = {
        'path': _list_thumbnail
    }


init_login()
admin = admin.Admin(app, 'Auth', index_view=MyAdminIndexView())

admin.add_view(MyModelView(User))
admin.add_view(MyModelView(models.Entry))
admin.add_view(MyModelView(models.Page))
admin.add_view(ImageView(models.Image))
