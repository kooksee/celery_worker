import os
from os.path import abspath as ap, dirname as dn

from kervice.app.const import Env
from kervice.utils.app import Application


class Config(object):
    SECRET_KEY = '33456@#$456@#$12%^&*('
    ROOT_PATH = dn(dn(dn(ap(__file__))))

    # 可见性超时时间定义了等待职程在消息分派到其他职程之前确认收到任务的秒数。一定要阅读下面的 警示 一节。
    # 这个选项通过 BROKER_TRANSPORT_OPTIONS 设置:

    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # 1 hour.

    BROKER_URL = 'redis://127.0.0.1:6379/6'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/5'

    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = True

    # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
    CELERY_RESULT_SERIALIZER = 'json'

    # 指定接受的内容类型
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml', 'pickle']

    # 任务序列化和反序列化使用msgpack方案
    CELERY_TASK_SERIALIZER = 'msgpack'

    # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24

    MAIL_HOST = os.getenv("MAIL_HOST")  # 设置服务器
    MAIL_USER = os.getenv("MAIL_USER")  # 用户名
    MAIL_PASS = os.getenv("MAIL_PASS")  # 口令


class LocalConfig(Config):
    BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

    REDIS = {
        "host": "127.0.0.1",
        "port": 6379
    }


class DevConfig(Config):
    BROKER_URL = 'redis://192.168.202.205:9221/0'
    CELERY_RESULT_BACKEND = 'redis://192.168.202.205:9221/0'

    REDIS = {
        "password": None,
        "db": 0,
        "host": "192.168.202.205",
        "port": 9221

    }


class UatConfig(Config):
    BROKER_URL = 'redis://192.168.202.214:9221/0'
    CELERY_RESULT_BACKEND = 'redis://192.168.202.214:9221/0'

    REDIS = {
        "password": None,
        "db": 0,
        "host": "192.168.202.214",
        "port": 9221
    }


class ProConfig(Config):
    BROKER_URL = 'redis://172.16.10.19:9221/0'
    CELERY_RESULT_BACKEND = 'redis://172.16.10.19:9221/0'

    REDIS = {
        "password": None,
        "db": 0,
        "host": "172.16.10.19",
        "port": 9221
    }


def init_config():
    app = Application.current()

    _e = app.env
    if _e == Env.local:
        _f = LocalConfig()
    elif _e == Env.dev:
        _f = DevConfig()
    elif _e == Env.uat:
        _f = UatConfig()
    elif _e == Env.production:
        _f = ProConfig()
    else:
        _f = LocalConfig()

    app.config = _f
