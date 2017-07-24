from gevent import monkey

monkey.patch_all()

import os
import sys
from os.path import abspath as ap, dirname as dn

sys.path.append(dn(dn(ap(__file__))))

from kervice.utils import when
from kervice.utils.app import Application
from kervice.app.const import Env
from kervice.app.main import init_app

app = Application.instance()
app.env = os.getenv("SERVICE_ENV", Env.local)
app.root_path = dn(dn(ap(__file__)))
app.name = os.getenv("SERVICE_NAME", None) or "test"
print(app.name)
app.debug = when(app.env == Env.production, False, True)


from kervice.utils.log_util import KLog
from kervice.bussiness.log import log_callback

KLog(callback=log_callback).init_log()
init_app()

app.config_from_object(app.config)

if __name__ == "__main__":
    app.start()
