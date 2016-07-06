import tornado
from .handlers import *

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/newspark", SparkHandler),
], debug=True)
