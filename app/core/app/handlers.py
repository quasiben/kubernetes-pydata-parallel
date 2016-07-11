import time

import tornado
import tornado.web
from tornado import gen
from tornado.log import app_log
from tornado.ioloop import IOLoop

from .. import config
from ..pod import gen_available_name
from ..namespaces import NameSpace
from ..services import Service
from ..replicationcontroller import ReplicationController

from core import Kubernetes, Proxy

kube = Kubernetes(config.KUBERNETES_API, username=config.KUBERNETES_USERNAME, password=config.KUBERNETES_PASSWORD)
proxy = Proxy.from_kubernetes(kube)


@gen.coroutine
def wait_for_running_pods(kube, namespace, timeout=10):
    time = IOLoop.current().time
    start = time()
    pods = kube.list_pods(namespace=namespace)
    app_log.info("Waiting for %s to be running", namespace)
    while any(pod.status.phase != "Running" for pod in pods):
        app_log.info("%s %s", namespace, [ p.status.phase for p in pods ])
        if time() - start > timeout:
            raise TimeoutError()
        yield gen.sleep(1)
        pods = kube.list_pods(namespace=namespace)
    return pods


class MainHandler(tornado.web.RequestHandler):

    def get_app_id(self, container_spec):
        env_variables = container_spec.containers[0].env
        for env_var in env_variables:
            if env_var.name == "APP_ID":
                return env_var.value

    def get(self):
        self.render("templates/index.html")


class WaitHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, app_id):
        try:
            yield wait_for_running_pods(kube, app_id + '-ns')
        except TimeoutError:
            # not done, set 202
            self.set_status(202)
            return

        for i in range(10):
            print(app_id, proxy.app_id_exists(app_id))
            if not proxy.app_id_exists(app_id):
                app_log.info("Waiting for app to show up in the proxy")
                yield gen.sleep(1)
            else:
                break

        app_url = "{url}/".format(url=proxy.lookup(app_id))
        app_log.info("JUPYTER APP URL: %s", app_url)
        self.finish(app_url)

class AllServices(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.render('templates/spawn.html')

    @gen.coroutine
    def post(self):
        from ..pod import DaskSchedulerContainer

        # name = "donothing"
        proxy_name = gen_available_name(prefix="dask-app", proxy=proxy)
        ns = NameSpace(name=proxy_name+'-ns')
        kube.create_namespace(ns)

        git_url = 'https://github.com/mrocklin/scipy-2016-parallel.git'
        dask_scheduler_container = DaskSchedulerContainer(proxy_name, git_url,
                                                          proxy=proxy,
                                                          add_pod_ip_env=True)

        # create dask-scheduler
        rpc_master = ReplicationController('dask-scheduler-controller')
        rpc_master.set_selector('schedulers')

        rpc_master.add_containers(dask_scheduler_container)
        kube.create_replication_controller(rpc_master, ns.name)
        self.set_status(202)
        self.finish(proxy_name)
        yield self.finish_spawning(ns, dask_scheduler_container)
    
    @gen.coroutine
    def finish_spawning(self, ns, dask_scheduler_container):
        from ..pod import DaskWorkerContainer

        yield gen.sleep(2)

        # create dask-cluster service
        serv = Service('schedulers')
        serv.add_port(7077, 7077, 'spark-master-port')
        serv.add_port(9000, 9000, 'scheduler-port')
        serv.add_port(9001, 9001, 'http-port')
        serv.add_port(9002, 9002, 'bokeh-port')
        serv.add_port(10000, 10000, 'ip-registration')
        serv.add_port(10101, 10101, 'ip-engines1')
        serv.add_port(10102, 10102, 'ip-engines2')
        serv.add_port(10103, 10103, 'ip-engines3')
        serv.add_port(10104, 10104, 'ip-engines4')
        serv.add_port(10105, 10105, 'ip-engines5')
        serv.add_port(10106, 10106, 'ip-engines6')

        kube.create_service(serv, ns.name)

        yield gen.sleep(2)

        # create dask-worker/spark-worker/ipengines
        rpc_worker = ReplicationController('dask-worker-controller')
        rpc_worker.set_replicas(8)
        rpc_worker.set_selector('dask-worker')

        dask_work_container = DaskWorkerContainer('dask-worker', add_pod_ip_env=False)

        rpc_worker.add_containers(dask_work_container)

        aa = kube.create_replication_controller(rpc_worker, ns.name)
