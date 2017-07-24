def init_url():
    from kervice.utils.app import Application
    app = Application.current()

    from kervice.app.handlers import debug_task
    app.task(bind=True,name="test.hello")(debug_task)

    from celery.task import periodic_task
    from celery.schedules import crontab
    from kervice.app.handlers import every_morning
    periodic_task(run_every=crontab(hour=7, minute=30))(every_morning)
