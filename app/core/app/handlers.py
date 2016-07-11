import time

import tornado
import tornado.web
from tornado import gen
from tornado.ioloop import IOLoop

from .. import config
from ..pod import gen_available_name
from ..namespaces import NameSpace
from ..services import Service
from ..replicationcontroller import ReplicationController

from core import Kubernetes, Proxy

kube = Kubernetes(config.KUBERNETES_API, username=config.KUBERNETES_USERNAME, password=config.KUBERNETES_PASSWORD)
proxy = Proxy.from_kubernetes(kube)


def wait_for_running_pod(kube, pod_name):
    pod = kube.get_pod(name=pod_name)
    while pod.status.phase != "Running":
        print("Waiting for container to be running")
        yield gen.Task(IOLoop.instance().add_timeout, time.time() + 2)
        pod = kube.get_pod(name=pod_name)
    return pod


class MainHandler(tornado.web.RequestHandler):

    def get_app_id(self, container_spec):
        env_variables = container_spec.containers[0].env
        for env_var in env_variables:
            if env_var.name == "APP_ID":
                return env_var.value

    def get(self):
        self.render("templates/index.html")


class AllServices(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        from ..pod import DaskSchedulerContainer
        from ..pod import DaskWorkerContainer

        # name = "donothing"
        proxy_name = gen_available_name(prefix="dask-app", proxy=proxy)
        ns = NameSpace(name=proxy_name+'-ns')
        kube.create_namespace(ns)

        # create dask-scheduler
        rpc_master = ReplicationController('dask-scheduler-controller')
        rpc_master.set_selector('schedulers')

        git_url = 'https://github.com/mrocklin/scipy-2016-parallel.git'
        dask_scheduler_container = DaskSchedulerContainer(proxy_name, git_url,
                                                          proxy=proxy,
                                                          add_pod_ip_env=True)

        rpc_master.add_containers(dask_scheduler_container)
        kube.create_replication_controller(rpc_master, ns.name)

        time.sleep(2)

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

        time.sleep(2)

        # create dask-worker/spark-worker/ipengines
        rpc_worker = ReplicationController('dask-worker-controller')
        rpc_worker.set_replicas(8)
        rpc_worker.set_selector('dask-worker')

        dask_work_container = DaskWorkerContainer('dask-worker', add_pod_ip_env=False)

        rpc_worker.add_containers(dask_work_container)

        aa = kube.create_replication_controller(rpc_worker, ns.name)

        pod_name = dask_scheduler_container.name
        created_pod = wait_for_running_pod(kube, pod_name)

        app_url = "{url}/".format(url=proxy.lookup(pod_name))
        print("JUPYTER APP URL:", app_url)
        self.write("Jupyter notebook running at: <a href=\"{0}\">{0}</a>".format(app_url))
        self.finish()
