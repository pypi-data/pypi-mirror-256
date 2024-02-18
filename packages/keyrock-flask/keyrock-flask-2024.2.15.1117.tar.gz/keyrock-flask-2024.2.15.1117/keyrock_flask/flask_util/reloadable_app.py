import logging
logger = logging.getLogger(__name__)

try:
    import flask
except Exception as e:
    logger.warning(e)


class ReloadableApp(object):
    def __init__(self, create_app_func, get_version_func):
        self.create_app_func = create_app_func
        self.get_version_func = get_version_func
        self.app = create_app_func()
        self.cfg_ver = get_version_func()
        # def get_version_func():
        #     return service.redis.get('cfg_ver')

    def get_application(self):
        cfg_ver = self.get_version_func()
        to_reload = cfg_ver != self.cfg_ver
        if to_reload:
            logger.warning('Reloading server on request. {0} to {1}'.format(self.cfg_ver, cfg_ver))
            self.cfg_ver = cfg_ver
            self.app = self.create_app_func()

        return self.app

    def __call__(self, environ, start_response):
        app = self.get_application()
        return app(environ, start_response)
