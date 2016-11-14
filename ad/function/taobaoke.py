# coding=utf-8
from __future__ import unicode_literals, absolute_import

import pyexcel as pe

from AutoSystem.settings import TAOBAOKE_EXCEL_FILE

__author__ = 'GoTop'

def import_taobaoke_excel():


    records = pe.iget_records(file_name=TAOBAOKE_EXCEL_FILE)
    for record in records:
       print("%s is aged at %d" % (record['Name'], record['Age']))
    return records
