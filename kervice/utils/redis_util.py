from threading import Timer

import gevent
import redis
import redis.connection
from gevent import socket as gsocket

from kervice.utils import pp
from kervice.utils import red

redis.connection.socket = gsocket


class RedisManager(object):
    def __init__(self, config=None):
        self.config = config
        self.__r = None
        self.__t = Timer(2, self.__conn)

    def __conn(self):
        try:
            self._conn().get('__test')
            if self.__t.is_alive():
                self.__t.cancel()
        except Exception as e:
            pp("redis 链接失败：{}".format(e), red, print)

    def conn(self):
        try:
            _r = self._conn()
            _r.get('__test')
            return _r
        except Exception as e:
            print(e)

            if not self.__t.is_alive():
                self.__t.start()

    def _conn(self):
        _r = self.config
        host = _r.get("host")
        port = _r.get("port")
        password = _r.get("password")
        db = _r.get("db", 0)
        kwargs = _r.get("kwargs", {})

        return redis.Redis(connection_pool=redis.ConnectionPool(
            host=host, port=port, db=db, password=password, **kwargs
        ))


def init_redis():
    from kervice.utils.app import Application
    app = Application.current()
    app.redis = RedisManager(config=app.config.REDIS)


def _main(i):
    r = RedisManager(config={"host": 'localhost', "port": 6379}).conn()

    while 1:
        if not r:
            gevent.sleep(1)
            continue

        _res = r.hset('ss', 'dd', u"ss")
        print(_res)
        print(str(r.hget('ss', 'dd')))
        print(i, "\n\n")
        gevent.sleep(1)


def _main1():
    r = RedisManager(config={"host": 'localhost', "port": 6679}).conn()
    while 1:
        if not r:
            print("ok")
            gevent.sleep(0.5)
            continue
        r.get('ss')
        _res = r.hset('ss', 'dd', u"过后就那么快就结婚过")
        print(_res)
        print(str(r.hget('ss', 'dd')))
        print(u"过后就那么快就结婚过")
        gevent.sleep(0.5)


if __name__ == '__main__':
    for i in range(100):
        gevent.spawn(_main, i).start()
    _main1()
