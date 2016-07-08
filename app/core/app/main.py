import tornado
from .handlers import *

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/newspark", SparkHandler),
    (r"/newdask", DaskHandler),
    (r"/newipyparallel", IPythonParallelHandler),
    (r"/new_dasknamespace", DaskNameSpaceHandler),
], debug=True)
