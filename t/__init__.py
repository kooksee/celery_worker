import time

import gevent
from celery import Celery

app = Celery("clients", broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@app.task(name="test.hello", bind=True)
def f(self):
    print("ok")


while 1:
    _a = time.time()
    a = app.send_task('test.hello')
    # print(f.apply_async().get())
    print(a.get())
    print(time.time() - _a)

    gevent.sleep(0.1)

# flower --port=5555 --broker=redis://127.0.0.1:6379/0