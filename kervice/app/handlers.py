import ujson as json


def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    return json.dumps({
        "status": "ok"
    })


def every_morning():
    print("This is run every morning at 7:30")
