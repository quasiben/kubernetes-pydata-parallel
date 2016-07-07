import tornado
from .handlers import *

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/newspark", SparkHandler),
    (r"/newdask", DaskHandler),
    (r"/newipyparallel", IPythonParallelHandler),
], debug=True)
