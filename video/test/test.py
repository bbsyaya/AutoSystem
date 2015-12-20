# coding=utf-8
#from __future__ import unicode_literals
import base64

__author__ = 'GoTop'

token = 'XhCIj6hRoE6SH3wvQD5bezoxNDUwNDk0NTYw'
decoded = base64.urlsafe_b64decode(token)
print(decoded)

