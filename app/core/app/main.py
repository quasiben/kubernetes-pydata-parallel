import tornado
from .handlers import *

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/new_allservices", AllServices),
], debug=True)
