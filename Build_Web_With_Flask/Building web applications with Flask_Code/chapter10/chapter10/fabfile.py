# coding:utf-8

from fabric.api import *
from fabric.contrib.files import exists

env.linewise = True
# forward_agent allows you to git pull from your repository
# if you have your ssh key setup
env.forward_agent = True
env.hosts = ['your.host.ip.address']


def create_project():
    if not exists('~/project'):
        run('git clone git://path/to/repo.git')


def update_code():
    with cd('~/project'):
        run('git pull')


def reload():
    "Reloads project instance"
    run('touch --no-dereference /tmp/reload')
