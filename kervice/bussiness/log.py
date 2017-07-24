import logging
import sys
import ujson as json

from kervice.utils import colors

log = logging.getLogger(__name__)
from kervice.utils.app import Application


async def __log_post(data):
    """
    data:{
        "cnt": "内容: text",
        "name": "服务名字: text"
    }

    :param data:
    :return:
    """

    name = data.get("name", "test")
    cnt = data.get("cnt", {})

    app = Application.current()

    st, col = app.mongo.col(name)
    result = await col.insert_one(cnt)
    print('result %s' % repr(result.inserted_id))


def log_callback(record):
    app = Application.current()

    _msg = record['msg']
    _c = colors.red if record.get("levelname") == "ERROR" else colors.blue
    if isinstance(_msg, dict):
        _r = app.redis.conn()
        if not _r:
            sys.stdout.write(
                colors.yellow(
                    "[{name}] [{asctime} {host_ip}] {filename}[{module}.{funcName}][{lineno}]\n".format(
                        **record
                    )
                )
            )
            sys.stdout.write(_c("{levelname}: {msg}\n".format(**record)))
        else:
            __name = "{}.log.error" if record.get("levelname") == "ERROR" else "{}.log.info"
            _r.hset('hset', __name.format(app.name), record.get("asctime"), json.dumps(record))

    else:
        sys.stdout.write(
            colors.yellow(
                "[{name}] [{asctime} {host_ip}] {filename}[{module}.{funcName}][{lineno}]\n".format(
                    **record
                )
            )
        )
        sys.stdout.write(_c("{levelname}: {msg}\n".format(**record)))
