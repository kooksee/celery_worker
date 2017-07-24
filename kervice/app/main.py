# -*- coding: utf-8 -*-
from uuid import uuid4

import gevent
from gevent.event import Event

from kervice.utils import pp
from kervice.utils.colors import yellow

event = Event()


def service_check():
    pp("info:\n  服务状态检测 ok", yellow, print)
    while True:
        try:

            print(uuid4())
            gevent.sleep(1)
        except Exception as e:
            print(e)


def init_app():
    # 初始化服务进程
    pp("info:\n  初始化服务", yellow, print)

    from kervice.app.config import init_config
    init_config()

    from kervice.utils.redis_util import init_redis
    init_redis()

    from kervice.app.urls import init_url
    init_url()

    gevent.spawn(service_check).start()

