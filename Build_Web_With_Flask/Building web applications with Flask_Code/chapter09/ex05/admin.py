# coding:utf-8

from flask import g
from flask.ext.login import current_user, login_required
from flask.ext.admin import Admin, AdminIndexView, expose
from flask.ext.admin.contrib.sqla import ModelView

from permissions import *


class AuthMixinView(object):
    def is_accessible(self):
        has_auth = current_user.is_authenticated()
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm


class AuthModelView(AuthMixinView, ModelView):
    @expose()
    @login_required
    def index_view(self):
        return super(ModelView, self).index_view()


class AuthAdminIndexView(AuthMixinView, AdminIndexView):
    @expose()
    @login_required
    def index_view(self):
        return super(AdminIndexView, self).index_view()


admin = Admin(name='Administrative Interface', index_view=AuthAdminIndexView())
