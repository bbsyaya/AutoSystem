# coding=utf8
from __future__ import unicode_literals
from unicodedata import normalize

__author__ = 'GoTop'


def slug(text, encoding=None, permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):
    '''
    自动生成slug
    来源： https://gist.github.com/turicas/1428479
    :param text:
    :param encoding:
    :param permitted_chars:
    :return:
    '''
    if isinstance(text, str):
        text = text.decode(encoding or 'ascii')
    clean_text = text.strip().replace(' ', '-').lower()
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)
    return ''.join(strict_text)