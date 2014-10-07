# coding=utf-8
from __future__ import unicode_literals
from os.path import dirname

__author__ = 'GoTop'

import sys
import os
from datetime import date, datetime, timedelta
import codecs
import ConfigParser


iswindows = 'win32' in sys.platform.lower() or 'win64' in sys.platform.lower()
isosx = 'darwin' in sys.platform.lower()
isfreebsd = 'freebsd' in sys.platform.lower()
islinux = not (iswindows or isosx or isfreebsd)


class KRConfig():
    '''提供封装好的配置'''

    def __init__(self, configfile=None):
        config = ConfigParser.ConfigParser()

        try:
            config.readfp(codecs.open(configfile, "r", "utf-8-sig"))
        except:
            config.readfp(codecs.open(configfile, "r", "utf-8"))

        self.auto_exit = self.getauto_exit(config)
        self.thread_numbers = self.getthread_numbers(config)
        self.kindle_format = self.getkindle_format(config)
        self.timezone = self.gettimezone(config)
        self.grayscale = self.getgrayscale(config)
        self.kindlestrip = self.getkindlestrip(config)
        self.mail_enable = self.getmail_enable(config)
        self.mail_host = self.getmail_host(config)
        self.mail_port = self.getmail_port(config)
        self.mail_ssl = self.getmail_ssl(config)
        self.mail_from = self.getmail_from(config)
        self.mail_to = self.getmail_to(config)
        self.mail_username = self.getmail_username(config)
        self.mail_password = self.getmail_password(config)
        self.user = self.getuser(config)
        self.max_items_number = self.getmax_items_number(config)
        self.max_image_per_article = self.getmax_image_per_article(config)
        self.max_old_date = self.getmax_old_date(config)
        self.feeds = self.getfeeds(config)
        self.kindlegen = self.find_kindlegen_prog()
        self.work_dir = self.getwork_dir()

    def getauto_exit(self, config=None):
        try:
            return int(config.get('general', 'auto_exit').strip())
        except:
            return 1

    def getthread_numbers(self, config=None):
        try:
            return int(config.get('general', 'thread_numbers').strip())
        except:
            return 5

    def getkindle_format(self, config=None):
        try:
            format = str(config.get('general', 'kindle_format').strip())
            if format in ['book', 'periodical']:
                return format
            else:
                return 'book'
        except:
            return 'book'

    def gettimezone(self, config=None):
        try:
            return timedelta(hours=(int(config.get('general', 'timezone').strip())))
        except:
            return timedelta(hours=8)

    def getgrayscale(self, config=None):
        try:
            return int(config.get('general', 'grayscale').strip())
        except:
            return 0

    def getkindlestrip(self, config=None):
        try:
            return int(config.get('general', 'kindlestrip').strip())
        except:
            return 1

    def getmail_host(self, config=None):
        try:
            return str(config.get('mail', 'host').strip())
        except:
            return None

    def getmail_port(self, config=None):
        try:
            return int(config.get('mail', 'port').strip())
        except:
            return 25

    def getmail_ssl(self, config=None):
        try:
            return int(config.get('mail', 'ssl').strip())
        except:
            return 0

    def getmail_from(self, config=None):
        try:
            return str(config.get('mail', 'from').strip())
        except:
            return None

    def getmail_to(self, config=None):
        try:
            return str(config.get('mail', 'to').strip())
        except:
            return None

    def getmail_username(self, config=None):
        try:
            return str(config.get('mail', 'username').strip())
        except:
            return None

    def getmail_password(self, config=None):
        try:
            return str(config.get('mail', 'password').strip())
        except:
            return None

    def getmail_enable(self, config=None):
        try:
            return int(config.get('mail', 'mail_enable').strip())
        except:
            return 0

    def getuser(self, config=None):
        try:
            return str(config.get('reader', 'username').strip())
        except:
            return "user"

    def getmax_items_number(self, config=None):
        try:
            return int(config.get('reader', 'max_items_number').strip())
        except:
            return 5

    def getmax_image_per_article(self, config=None):
        try:
            return int(config.get('reader', 'max_image_per_article').strip())
        except:
            return 10

    def getmax_old_date(self, config=None):
        try:
            return timedelta(int(config.get('reader', 'max_old_date').strip()))
        except:
            return timedelta(3)

    def getfeeds(self, config=None):
        try:
            feeds = [config.get("feeds", feeds_option).strip() for feeds_option in config.options("feeds")]
        except:
            feeds = []
        finally:
            return feeds

    def find_kindlegen_prog(self):
        '''find the path of kindlegen'''
        try:
            kindlegen_prog = 'kindlegen' + (iswindows and '.exe' or '')

            # search in current directory and PATH to find kinglegen
            sep = iswindows and ';' or ':'
            #将该文件的上一层绝对地址加入dirs中
            dirs = [dirname(os.path.split(os.path.realpath(__file__))[0]),]
            dirs.extend(os.getenv('PATH').split(sep))
            for dir in dirs:
                if dir:
                    fname = os.path.join(dir, kindlegen_prog)
                    if os.path.exists(fname):
                        # print fname
                        return fname
        except:
            return None

    def getwork_dir(self):
        try:
            #以当前文件的上一级目录为work_dir
            return dirname(os.path.split(os.path.realpath(__file__))[0])
        except:
            return None