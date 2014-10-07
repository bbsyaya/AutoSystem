# coding=utf-8
#!/usr/bin/env python

"""
KindleReader
Created by Jiedan<lxb429@gmail.com> on 2010-11-08.
"""
from __future__ import unicode_literals


__author__ = ["Jiedan<lxb429@gmail.com>", "williamgateszhao<williamgateszhao@gmail.com>"]
__version__ = "0.6.5"

import sys
import os
import time
import hashlib
import re
import string
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import parsedate_tz
from datetime import date, datetime, timedelta

import subprocess
import Queue, threading
import socket, urllib2, urllib
from lib import smtplib
from lib.tornado import escape
from lib.tornado import template
from lib.BeautifulSoup import BeautifulSoup
from lib.kindlestrip import SectionStripper
from lib import feedparser

from function.template import *
from function.read_config import KRConfig

# 不加入以下设置，从数据库中读取出非ascii的字符串将会提示编码错误
reload(sys)
sys.setdefaultencoding('utf8')

try:
    from PIL import Image
except ImportError:
    Image = None

socket.setdefaulttimeout(20)
imgq = Queue.Queue(0)
feedq = Queue.Queue(0)
updated_feeds = []
feedlock = threading.Lock()


class feedDownloader(threading.Thread):
    '''多线程下载并处理feed'''

    remove_tags = ['script', 'object', 'video', 'embed', 'iframe', 'noscript', 'style']
    remove_attributes = ['class', 'id', 'title', 'style', 'width', 'height', 'onclick']

    def __init__(self, threadname, config):
        # 注意：使用这种方式创建进程时，一定要显式的调用父类的初始化函数。
        threading.Thread.__init__(self, name=threadname)
        self.krconfig = config


    def run(self):
        # 通过继承Thread类，重写它的run方法来创建线程
        # 重写父类run方法，在线程启动后执行该方法内的代码。
        global feedq

        while True:
            i = feedq.get()
            feed_data, force_full_text = self.getfeed(i['feed'])
            if feed_data:
                self.makelocal(feed_data, i['feed_idx'], force_full_text)
            else:
                pass
            feedq.task_done()

    def getfeed(self, feed):
        """access feed by url"""
        force_full_text = 0
        try:
            # 如果config里在feed的url前设置了full字样
            if feed[0:4] == 'full':
                force_full_text = 1
                feed_data = self.parsefeed(feed[4:])
                if feed_data:
                    return feed_data, force_full_text
                else:
                    raise UserWarning("illegal feed:{}".format(feed))
            else:
                # 没设置full字样时
                feed_data = self.parsefeed(feed)
                if feed_data:
                    return feed_data, force_full_text
                else:
                    raise UserWarning("illegal feed:{}".format(feed))
        except Exception, e:
            logging.error("fail:({}):{}".format(feed, e))
            return None, None

    def parsefeed(self, feed, retires=1):
        """parse feed using feedparser"""
        try:  # 访问feed，自动尝试在地址结尾加上或去掉'/'
            feed_data = feedparser.parse(feed.encode('utf-8'))
            if not feed_data.feed.has_key('title'):
                if feed[-1] == '/':
                    feed_data = feedparser.parse(feed[0:-1].encode('utf-8'))
                elif feed[-1] != '/':
                    feed_data = feedparser.parse((feed + '/').encode('utf-8'))
                if not feed_data.feed.has_key('title'):
                    raise UserWarning("read error")
                else:
                    return feed_data
            else:
                return feed_data
        except UserWarning:
            logging.error("fail({}): {}".format(feed, "read error"))
            return None
        except Exception, e:
            if retires > 0:
                logging.error("error({}): {} , retry".format(feed, e))
                return self.parsefeed(feed, retires - 1)  # 如果读取错误，重试一次
            else:
                logging.error("fail({}): {}".format(feed, e))
                return None

    def makelocal(self, feed_data, feed_idx, force_full_text=0):
        '''生成解析结果'''
        global imgq
        global updated_feeds
        global feedlock

        try:
            local = {
                'idx': feed_idx,
                'entries': [],
                'title': feed_data.feed['title'],
            }

            item_idx = 1
            for entry in feed_data.entries:
                if item_idx > self.krconfig.max_items_number:
                    break

                try:
                    published_datetime = datetime(*entry.published_parsed[0:6])
                except:
                    if 'published' in entry:
                        published_datetime = self.parsetime(entry.published)
                    else:
                        # todo 会报错
                        published_datetime = None

                # 时间超过config里设定的max_old_date的就不再使用来生成mobi了
                if datetime.utcnow() - published_datetime > self.krconfig.max_old_date:
                    break

                try:
                    if entry.author:
                        local_author = entry.author
                    else:
                        local_author = "anonymous"
                except:
                    local_author = "anonymous"

                local_entry = {
                    'idx': item_idx,
                    'title': entry.title,
                    'published': (published_datetime + self.krconfig.timezone).strftime("%Y-%m-%d %H:%M:%S"),
                    'url': entry.link,
                    'author': local_author,
                }

                if force_full_text:
                    # 如果设置了获取rss的全文
                    local_entry['content'], images = self.force_full_text(entry.link)
                else:
                    # 如果没设置获取rss的全文
                    try:
                        local_entry['content'], images = self.parse_summary(entry.content[0].value, entry.link)
                    except:
                        local_entry['content'], images = self.parse_summary(entry.summary, entry.link)

                local_entry['stripped'] = ''.join(
                    BeautifulSoup(local_entry['content'], convertEntities=BeautifulSoup.HTML_ENTITIES).findAll(
                        text=True))[:200]

                local['entries'].append(local_entry)

                # 将这篇文章中的图片存入imgq队列中
                for i in images:
                    imgq.put(i)
                item_idx += 1

            if len(local['entries']) > 0:
                # 获取feedlock锁对象，往updated_feeds里添加整理好的一个feed的信息时
                if feedlock.acquire():
                    # updated_feeds为全局变量
                    updated_feeds.append(local)
                    feedlock.release()
                else:
                    feedlock.release()
                logging.info("from feed{} update {} items.".format(feed_idx, len(local['entries'])))
            else:
                logging.info("feed{} has no update.".format(feed_idx))
        except Exception, e:
            logging.error("fail(feed{}): {}".format(feed_idx, e))

    def parsetime(self, strdatetime):
        '''尝试处理feedparser未能识别的时间格式'''
        try:
            # 针对Mon,13 May 2013 06:48:25 GMT+8这样的奇葩格式
            if strdatetime[-5:-2] == 'GMT':
                t = datetime.strptime(strdatetime[:-6], '%a,%d %b %Y %H:%M:%S')
                return (t - timedelta(hours=int(strdatetime[-2:-1])) + self.krconfig.timezone)
            # feedparser对非utc时间的支持有问题（Wes, 22 May 2013 13:54:00 +0800这样的）
            elif (strdatetime[-5:-3] == '+0' or strdatetime[-5:-3] == '-0') and strdatetime[-2:] == '00':
                a = parsedate_tz(strdatetime)
                t = datetime(*a[:6]) - timedelta(seconds=a[-1])
                return (t + self.krconfig.timezone)
            else:
                return (datetime.utcnow() + self.krconfig.timezone)
        except Exception, e:
            return (datetime.utcnow() + self.krconfig.timezone)

    def force_full_text(self, url):
        '''当需要强制全文输出时，将每个entry单独发给fivefilters'''
        logging.info("(force full text):{}".format(url))
        fulltextentry = self.parsefeed('http://ftr.fivefilters.org/makefulltextfeed.php?url=' + url)
        if fulltextentry:
            return self.parse_summary(fulltextentry.entries[0].summary, url)
        else:
            try:
                return self.parse_summary(entry.content[0].value, url)
            except:
                return self.parse_summary(entry.summary, url)

    def parse_summary(self, summary, ref):
        """处理文章内容，去除多余标签并处理图片地址"""

        soup = BeautifulSoup(summary)

        for span in list(soup.findAll(attrs={"style": "display: none;"})):
            span.extract()

        for attr in self.remove_attributes:
            for x in soup.findAll(attrs={attr: True}):
                del x[attr]

        for tag in soup.findAll(self.remove_tags):
            tag.extract()

        img_count = 0
        images = []
        for img in list(soup.findAll('img')):
            # 如果<img>标签中没有src地址，就将其去除
            if (self.krconfig.max_image_per_article >= 0 and img_count >= self.krconfig.max_image_per_article) \
                    or img.has_key('src') is False:
                #PageElement.extract() removes a tag or string from the tree.
                #It returns the tag or string that was extracted
                img.extract()
            else:
                try:
                    if img['src'].encode('utf-8').lower().endswith(('jpg', 'jpeg', 'gif', 'png', 'bmp')):
                        #处理img标签的src并映射到本地文件
                        localimage, fullname = self.parse_image(img['src'])
                        # 确定结尾为图片后缀，防止下载非图片文件（如用于访问分析的假图片）
                        if os.path.isfile(fullname) is False:
                            images.append({
                                'url': img['src'],
                                'filename': fullname,
                                'referer': ref
                            })
                        if localimage:
                            img['src'] = localimage
                            img_count = img_count + 1
                        else:
                            img.extract()
                    else:
                        img.extract()
                except Exception, e:
                    logging.info("error: %s" % e)
                    img.extract()

        return soup.renderContents('utf-8'), images

    def parse_image(self, url, filename=None):
        """处理img标签的src并映射到本地文件"""
        url = escape.utf8(url)
        image_guid = hashlib.sha1(url).hexdigest()

        x = url.split('.')
        ext = 'jpg'
        if len(x) > 1:
            ext = x[-1]

            if len(ext) > 4:
                ext = ext[0:3]

            ext = re.sub('[^a-zA-Z]', '', ext)
            ext = ext.lower()

            if ext not in ['jpg', 'jpeg', 'gif', 'png', 'bmp']:
                ext = 'jpg'

        y = url.split('/')
        h = hashlib.sha1(str(y[2])).hexdigest()

        hash_dir = os.path.join(h[0:1], h[1:2])
        filename = image_guid + '.' + ext

        img_dir = os.path.join(self.krconfig.work_dir, 'data', 'images', hash_dir)
        fullname = os.path.join(img_dir, filename)

        if not os.path.exists(img_dir):
            os.makedirs(img_dir)

        localimage = 'images/%s/%s' % (hash_dir, filename)
        return localimage, fullname


class ImageDownloader(threading.Thread):
    '''多线程下载图片'''

    def __init__(self, threadname, config):
        threading.Thread.__init__(self, name=threadname)
        self.krconfig = config

    def run(self):
        global imgq

        while True:
            # 从imgq队列中获取图片信息，然后下载
            i = imgq.get()
            self.getimage(i)
            imgq.task_done()

    def getimage(self, i, retires=1):
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                'Referer': i['referer']
            }
            req = urllib2.Request(
                url=i['url'].encode('utf-8'),
                headers=header
            )
            opener = urllib2.build_opener()
            response = opener.open(req, timeout=30)
            with open(i['filename'], 'wb') as img:
                img.write(response.read())
            if Image and self.krconfig.grayscale == 1:
                try:
                    img = Image.open(i['filename'])
                    new_img = img.convert("L")
                    new_img.save(i['filename'])
                except:
                    pass
            logging.info("download: {}".format(i['url'].encode('utf-8')))
        except urllib2.HTTPError as http_err:
            if retires > 0:
                return self.getimage(i, retires - 1)
            logging.info("HttpError: {},{}".format(http_err, i['url'].encode('utf-8')))
        except Exception, e:
            if retires > 0:
                return self.getimage(i, retires - 1)
            logging.error("Failed: {}".format(e, i['url'].encode('utf-8')))


class KindleReader():
    """core of KindleReader"""

    def __init__(self, feeds=[]):
        self.feeds = feeds
        self.work_dir = os.path.split(os.path.realpath(__file__))[0]

        logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(msecs)03d %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M')

        self.check()
        st = time.time()
        logging.info("welcome, start ...")

        try:
            self.main()
        except Exception, e:
            logging.info("Error: %s " % e)

        logging.info("used time {}s".format(time.time() - st))
        logging.info("done.")

        if not self.krconfig.auto_exit:
            raw_input("Press any key to exit...")


    def sendmail(self, data):
        """send html to kindle"""

        if not self.krconfig.mail_from:
            raise Exception("'mail from' is empty")

        if not self.krconfig.mail_to:
            raise Exception("'mail to' is empty")

        if not self.krconfig.mail_host:
            raise Exception("'mail host' is empty")

        logging.info("send mail to {} ... ".format(self.krconfig.mail_to))

        msg = MIMEMultipart()
        msg['from'] = self.krconfig.mail_from
        msg['to'] = self.krconfig.mail_to
        msg['subject'] = 'Convert'

        htmlText = 'kindle reader delivery.'
        msg.preamble = htmlText

        msgText = MIMEText(htmlText, 'html', 'utf-8')
        msg.attach(msgText)

        att = MIMEText(data, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="kindle-reader-%s.mobi"' % (
            datetime.utcnow() + self.krconfig.timezone).strftime('%Y%m%d-%H%M%S')
        msg.attach(att)

        try:
            if self.krconfig.mail_ssl == 1:
                mail = smtplib.SMTP_SSL(timeout=60)
            else:
                mail = smtplib.SMTP(timeout=60)

            mail.connect(self.krconfig.mail_host, self.krconfig.mail_port)
            mail.ehlo()

            if self.krconfig.mail_username and self.krconfig.mail_password:
                mail.login(self.krconfig.mail_username, self.krconfig.mail_password)

            mail.sendmail(msg['from'], msg['to'], msg.as_string())
            mail.close()
        except Exception, e:
            logging.error("fail:%s" % e)

    def make_mobi(self, user, feeds, format='book'):
        """make a mobi file using kindlegen"""

        logging.info("generate .mobi file start... ")

        data_dir = os.path.join(self.work_dir, 'data')
        # data目录为存放生成的mobi文件的目录
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # 根据TEMPLATES字典中的key值（'content.html'，'toc.ncx'，'content.opf'）生成对应的文件
        for tpl in TEMPLATES:
            if tpl is 'book.html':
                continue

            t = template.Template(TEMPLATES[tpl])
            content = t.generate(
                user=user,
                feeds=feeds,
                format=format,
                mobitime=datetime.utcnow() + self.krconfig.timezone
            )

            with open(os.path.join(data_dir, tpl), 'wb') as fp:
                fp.write(content)

        mobi8_file = "KindleReader8-%s.mobi" % (datetime.utcnow() + self.krconfig.timezone).strftime('%Y%m%d-%H%M%S')
        mobi6_file = "KindleReader-%s.mobi" % (datetime.utcnow() + self.krconfig.timezone).strftime('%Y%m%d-%H%M%S')
        opf_file = os.path.join(data_dir, "content.opf")

        log_file = os.path.join(self.work_dir, "log.txt")
        subprocess.call('"%s" "%s" -o "%s" > %s' %
                        (self.krconfig.kindlegen, opf_file, mobi8_file, log_file), shell=True)

        # kindlegen生成的mobi，含有v6/v8两种格式
        mobi8_file = os.path.join(data_dir, mobi8_file)
        # kindlestrip处理过的mobi，只含v6格式
        mobi6_file = os.path.join(data_dir, mobi6_file)
        if self.krconfig.kindlestrip == 1:
            # 调用kindlestrip处理mobi
            try:
                data_file = file(mobi8_file, 'rb').read()
                strippedFile = SectionStripper(data_file)
                file(mobi6_file, 'wb').write(strippedFile.getResult())
                mobi_file = mobi6_file
            except Exception, e:
                mobi_file = mobi8_file
                logging.error("Error: %s" % e)
        else:
            mobi_file = mobi8_file

        if os.path.isfile(mobi_file) is False:
            logging.error("failed!")
            return None
        else:
            logging.info(".mobi save as: {}({}KB)".format(mobi_file, os.path.getsize(mobi_file) / 1024))
            return mobi_file

    def check(self):
        """
        检查config文件与kindlegen文件是否存在
        :rtype : object
        :return:
        """
        try:
            configfile = os.path.join(self.work_dir, "config.ini")
            self.krconfig = KRConfig(configfile=configfile)
        except:
            logging.error("config file {} not found or format error".format(os.path.join(work_dir, "config.ini")))
            sys.exit(1)

        if not self.krconfig.kindlegen:
            logging.error("Can't find kindlegen")
            sys.exit(1)

    # To use your method without an instance of a class you can attach a class method decorator like so
    def main(self):
        global imgq
        global feedq
        global updated_feeds

        feed_idx = 1

        # 读出config文件中设置的feed链接
        self.feeds.append(self.krconfig.feeds)
        feed_num = len(self.feeds)

        for feed in self.feeds:
            if feed[0:4] == 'full':
                logging.info("[{}/{}](force full text):{}".format(feed_idx, feed_num, feed[4:]))
            else:
                logging.info("[{}/{}]:{}".format(feed_idx, feed_num, feed))
            feedq.put({'feed': feed, 'feed_idx': feed_idx})
            feed_idx += 1

        feedthreads = []
        for i in range(self.krconfig.thread_numbers):
            f = feedDownloader('Threadfeed %s' % (i + 1), self.krconfig)
            feedthreads.append(f)
        for f in feedthreads:
            f.setDaemon(True)
            # run方法 和start方法: 它们都是从Thread继承而来的，run()方法将在线程开启后执行，
            # 可以把相关的逻辑写到run方法中（通常把run方法称为活动[Activity]。）；
            # start()方法用于启动线程。
            f.start()

        imgthreads = []
        for i in range(self.krconfig.thread_numbers):
            t = ImageDownloader('Threadimg %s' % (i + 1), self.krconfig)
            imgthreads.append(t)
        for t in imgthreads:
            t.setDaemon(True)
            t.start()

        feedq.join()
        imgq.join()

        if len(updated_feeds) > 0:
            mobi_file = self.make_mobi(self.krconfig.user, updated_feeds, self.krconfig.kindle_format)
            if mobi_file and self.krconfig.mail_enable == 1:
                fp = open(mobi_file, 'rb')
                self.sendmail(fp.read())
                fp.close()
        else:
            logging.info("no feed update.")


if __name__ == '__main__':
    KindleReader('')

    # logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(msecs)03d %(levelname)-8s %(message)s',
    # datefmt='%m-%d %H:%M')
    #
    # try:
    # work_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    # krc = KRConfig(configfile=os.path.join(work_dir, "config.ini"))
    # except:
    #     logging.error("config file {} not found or format error".format(os.path.join(work_dir, "config.ini")))
    #     sys.exit(1)
    #
    # if not krc.kindlegen:
    #     logging.error("Can't find kindlegen")
    #     sys.exit(1)
    #
    # st = time.time()
    # logging.info("welcome, start ...")
    #
    # try:
    #     kr = KindleReader(config=krc)
    #     kr.main()
    # except Exception, e:
    #     logging.info("Error: %s " % e)
    #
    # logging.info("used time {}s".format(time.time() - st))
    # logging.info("done.")
    #
    # if not krc.auto_exit:
    #     raw_input("Press any key to exit...")
