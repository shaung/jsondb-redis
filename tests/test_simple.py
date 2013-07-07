# -*- coding: utf-8 -*-

"""
    jsondb.tests
    ~~~~~~~~~~~~

    Tests for jsondb.
"""

import os, json
import jsondb
from jsondb.datatypes import *
from nose.tools import eq_

import logging
logging.basicConfig(level='DEBUG')

logger = logging.getLogger(__file__)



class TestBase:
    def eq_dumps(self, root_type, data):
        dbpath = 'redis://127.0.0.1:6379'
        db = jsondb.create(data, url=dbpath)
        db.close()
        db = jsondb.load(dbpath)
        eq_(db.dumps(), json.dumps(data))
        eq_(db.data(), data)


class TestSimpleTypes(TestBase):
    def test_string(self):
        self.eq_dumps(STR, 'Hello world!')
        self.eq_dumps(UNICODE, u'Hello world!')
        self.eq_dumps(STR, 'type')
        self.eq_dumps(STR, 'parent')
        self.eq_dumps(UNICODE, u'TYPE')

    def test_bool(self):
        self.eq_dumps(BOOL, True)
        self.eq_dumps(BOOL, False)
        self.eq_dumps(BOOL, 1)
        self.eq_dumps(BOOL, 0)

    def test_int(self):
        for i in xrange(100):
            self.eq_dumps(INT, i)

    def test_float(self):
        self.eq_dumps(FLOAT, 1.2)
        self.eq_dumps(FLOAT, 0.99999)
        self.eq_dumps(FLOAT, 0.00000000000000000001)

    def test_nil(self):
        self.eq_dumps(NIL, None)
 

if __name__ == '__main__':
    pass
