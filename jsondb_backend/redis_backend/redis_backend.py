# -*- coding: utf-8 -*-

import redis

from jsondb.backends.base import BackendBase
from jsondb.datatypes import *

"""
Redis backend
-------------

Hashes:
    jsondb:[dbid]:[rowid]
        id
        type
        value

Lists:
    jsondb:[dbid]:[rowid]:children

"""


class RedisBackend(BackendBase):
    def __init__(self, url, dbname=None, **kws):
        self.url = url
        self.dbname = dbname or 'default'
        self.conn = redis.StrictRedis(host=url.host,
                                      port=url.port or 6379,
                                      db=0)
        self.dbid = self._get_or_create_db()
        self.cntrkey = 'jsondb:%s:cntr' % self.dbid

    def _get_key(self, id):
        return 'jsondb:%s:%s' % (self.dbid, id)

    def _get_children_key(self, id):
        return 'jsondb:%s:%s:children' % (self.dbid, id)

    def get_cntr(self):
        cntr = self.conn.hget('jsondb', self.cntrkey)
        if cntr is None:
            self.conn.hset(self.cntrkey, 0)
            cntr = 0
        return cntr

    def _inc(self):
        return self.conn.hincrby('jsondb', self.cntrkey)

    def get_children_count(self, id):
        key = self._get_children_key(id)
        return self.conn.llen(key)

    def get_row(self, rowid):
        key = self._get_key(rowid)
        keys = self.conn.hkeys(key)
        values = self.conn.hvals(key)
        row = dict(zip(keys, values))
        print rowid, row
        print key
        _type = int(row['type'])
        row['type'] = _type
        if _type in (BOOL, INT):
            row['value'] = int(row['value'])
        elif _type == FLOAT:
            row['value'] = float(row['value'])
        return row
 
    def get_row_type(self, rowid):
        key = self._get_key(id)
        return int(self.conn.hget(key, 'type'))

    def get_nth_child(self, parent_id, offset):
        key = self._get_children_key(parent_id)
        child_id = self.conn.lindex(key, offset)
        if child_id is None:
            # TODO
            pass
        return self.get_row(child_id)

    def iter_children(self, parent_id, value=None, only_one=False):
        key = self._get_children_key(parent_id)
        for id in self.conn.lrange(key, 0, -1):
            yield self.get_row(id)


    def increase_value(self, id, increase_by=0):
        key = self._get_key(id)
        self.conn.hincrby(key, 'value', increase_by)

    def _gen_uuid(self):
        import uuid
        return uuid.uuid4()

    def _get_or_create_db(self):
        id = self.conn.hget('jsondb', self.dbname)
        if not id:
            id = self._gen_uuid()
            self.conn.hset('jsondb', self.dbname, id)
        return id

    def get_path(self):
        return str(self.url)
 
    def get_url(self):
        return str(self.url)
 
    def commit(self):
        pass
  
    def rollback(self):
        pass
 
    def close(self):
        pass

    def get_root_type(self):
        return int(self.conn.get('root_type'))
 
    def insert_root(self, (root_type, root)):
        key = self._get_key(-1)
        self.conn.hmset(key, {
            'id': -1,
            'parent': -2,
            'type': root_type,
            'value': root,
        })
        self.root_type = root_type
        print root
        print self.conn.hget(key, 'value')
        print key

    def insert(self, row):
        parent_id, type, value = row
        id = self._inc()
        key = self._get_key(id)
        self.conn.hmset(key, {
            'id': id,
            'parent': parent_id,
            'type': type,
            'value': value,
        })
        parent = self.get_row(parent_id)
        if parent['type'] == LIST:
            key = self._get_children_key(parent_id)
            self.conn.lpush(key, id)
        return id

    def batch_insert(self, *args, **kws):
        pass

    def update_link(self, *args, **kws):
        pass

    def jsonpath(self, *args, **kws):
        row = self._get_row(-1)
        yield Result.from_row(row)

    def dumprows(self, *args, **kws):
        pass

    def set_value(self, id, value):
        key = self._get_key(id)
        self.conn.hset(key, 'value', value)
