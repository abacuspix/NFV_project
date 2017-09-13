# coding:utf-8

from flask.ext.principal import RoleNeed, UserNeed, Permission
from flask.ext.principal import Principal

principal = Principal()

# admin permission role
admin_permission = Permission(RoleNeed('admin'))