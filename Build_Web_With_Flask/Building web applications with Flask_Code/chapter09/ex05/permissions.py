# coding:utf-8

from flask_principal import RoleNeed, UserNeed, Permission, Principal

principal = Principal()

# admin permission role
admin_permission = Permission(RoleNeed('admin'))