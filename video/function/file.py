# coding=utf-8
from __future__ import unicode_literals, absolute_import
import os

__author__ = 'GoTop'

def search_keyword_in_file(dir, keyword, extend=None):
    """
    查找dir目录下，文件名中包含keyword，后缀为extend的文件
    :param dir:
    :param keyword:
    :param extend:
    :return:
    """
    file_list = []
    for root, subFolders, files in os.walk(dir):
        for file in files:
            if extend is not None:
                # 如果设置了要查找文件的extend
                # string.find() 返回的是查找到的文本的位置，查找不成功过则返回-1
                if file.find(keyword) != -1 and file.endswith(extend):
                    file_list.append(os.path.join(dir, file))
            else:
                # 如果没设置要查找的extend
                if file.find(keyword) != -1:
                    file_list.append(os.path.join(dir, file))

    return file_list