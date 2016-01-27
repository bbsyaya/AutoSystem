# coding=utf-8
from __future__ import unicode_literals, absolute_import

from AutoSystem.celery import app

__author__ = 'GoTop'


@app.task
def add(x, y):
    return x + y
