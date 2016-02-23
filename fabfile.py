# coding=utf-8
from __future__ import unicode_literals, absolute_import

__author__ = 'GoTop'

from fabric.api import local, run, env, cd, hosts

code_dir = "/home/username/webapps/mysite/"
env.user = "username"

def work():
    local("workon AutoSystem")
    local("ssh-agent -s")
    local("set HOME=C/:\\Users\\GoTop")# 如果设置C:\\Users\\GoTop则不成功
    local("git fetch")
    local("git reset --hard origin/master")
    local("pip install -r requirements.txt")

def makem():
    local("python manage.py makemigrations")

def migrate():
    local("python manage.py migrate")


@hosts('localhost:8000')
def commit():
    #local("pip freeze > requirements.txt")
    message = raw_input("Enter a git commit message:  ")
    local("git add . && git commit -m \"%s\"" % message)
    local("git push origin master")

@hosts('xx.xxx.xxx.xx', 'xx.xxx.xxx.xx', 'xx.xxx.xxx.xx')
def deploy():
    with cd(code_dir):
        run("git pull origin master")
        run("touch mysite.wsgi")