import os
import tornado
from .handlers import *

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/new_allservices", AllServices),
    (r"/wait/(.*)", WaitHandler),
], debug=True, static_path=os.path.join(os.path.dirname(__file__), "templates", "static"))
