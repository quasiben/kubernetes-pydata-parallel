import tornado
import tornado.httpserver
from tornado import log
from core.app.main import application

log.enable_pretty_logging()
http_server = tornado.httpserver.HTTPServer(application, ssl_options={"certfile": "/tmp/ssl-cert.pem", "keyfile": "/tmp/ssl-key.pem",})
http_server.listen(8081, "0.0.0.0")
tornado.ioloop.IOLoop.current().start()
