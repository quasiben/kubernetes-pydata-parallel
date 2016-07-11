import tornado
from tornado import log
from core.app.main import application

log.enable_pretty_logging()
application.listen(8080, "0.0.0.0")
tornado.ioloop.IOLoop.current().start()
