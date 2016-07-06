import tornado
from core.app.main import application

application.listen(8080, "0.0.0.0")
tornado.ioloop.IOLoop.current().start()
