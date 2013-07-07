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
 

class TestLists:
    url = 'redis://127.0.0.1:6379'

    def test_list_create(self):
        """test list"""
        data = ['hello', 'world!', [1, 2.0]]
        db = jsondb.create(data, url=self.url)
        db.close()
        url = db.get_url()
        print url
        db = jsondb.load(url)
        eq_(db.data(), data)

    def test_list(self):
        """test list"""
        data = ['hello', 'world!', [1, 2.0]]
        db = jsondb.create([], url=self.url)
        for x in data:
            db.feed(x)
        db.close()
        url = db.get_url()
        print url
        db = jsondb.load(url)
        eq_(db.data(), data)

    def n_test_list_merge(self):
        """merge into a list"""

        data = ['initial item', 'added item1', 'item 2', 'item3-key']

        db = jsondb.create({}, url=self.url)
        _list_id = db.feed({'root' : data[:1]})[0]
        db.feed(data[1], _list_id)
        for x in data[2:]:
            db.feed(x, _list_id)
        db.close()
        url = db.get_url()
        print url

        db = jsondb.load(url)

        path = '$.root'
        rslt = db.query('$.root').values()
        eq_(rslt, [data])


if __name__ == '__main__':
    pass
