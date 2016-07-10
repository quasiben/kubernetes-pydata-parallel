import time

import tornado
import tornado.web
from tornado import gen
from tornado.ioloop import IOLoop

from .. import config
from ..pod import Pod
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
        # Get all containers
        pods = kube.list_pods().items
        pods = [c for c in pods if c.metadata.name.startswith(("jupyter",))]
        running_app_ids = [self.get_app_id(c.spec) for c in pods]

        # Clean routes for non-running apps
        proxy_app_ids = proxy.get_app_ids()
        for app_id in proxy_app_ids:
            if app_id not in running_app_ids:
                proxy.delete_route(app_id)
        #

        self.render("templates/index.html", pods=pods, lookup_url=proxy.lookup_url)


class SparkHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        git_url = "https://github.com/quasiben/kubernetes-scipy-2016.git"

        pod = Pod.from_jupyter_container(proxy, git_url)
        pod.add_spark_containers()
        kube.create_pod(pod)

        pod_name = pod.name
        created_pod = wait_for_running_pod(kube, pod_name)

        app_url = "{url}/".format(url=proxy.lookup(pod_name))
        print("JUPYTER APP URL:", app_url)
        self.write("Jupyter notebook running at: <a href=\"{0}\">{0}</a>".format(app_url))
        self.finish()


class DaskHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        git_url = "https://github.com/quasiben/kubernetes-scipy-2016.git"

        pod = Pod.from_jupyter_container(proxy, git_url)
        pod.add_dask_containers()
        kube.create_pod(pod)

        pod_name = pod.name
        created_pod = wait_for_running_pod(kube, pod_name)

        app_url = "{url}/".format(url=proxy.lookup(pod_name))
        print("JUPYTER APP URL:", app_url)
        self.write("Jupyter notebook running at: <a href=\"{0}\">{0}</a>".format(app_url))
        self.finish()


class IPythonParallelHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        git_url = "https://github.com/quasiben/kubernetes-scipy-2016.git"

        pod = Pod.from_jupyter_container(proxy, git_url)
        pod.add_ipyparallel_containers()
        kube.create_pod(pod)

        pod_name = pod.name
        created_pod = wait_for_running_pod(kube, pod_name)

        app_url = "{url}/".format(url=proxy.lookup(pod_name))
        print("JUPYTER APP URL:", app_url)
        self.write("Jupyter notebook running at: <a href=\"{0}\">{0}</a>".format(app_url))
        self.finish()


class DaskNameSpaceHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        from ..pod import SparkMasterContainer
        from ..pod import SparkWorkerContainer

        from uuid import uuid4

        name='bz-'+str(uuid4())
        ns = NameSpace(name=name)
        kube.create_namespace(ns)

        # create spark-cluster service
        serv = Service('spark-cluster')
        serv.add_port(7077, 7077)
        kube.create_service(serv, ns)

        rpc = ReplicationController('spark-master-controller')

        spark_master_container = SparkMasterContainer('spark-master')
        spark_master_container.add_port(8080)
        spark_master_container.image = 'gcr.io/continuum-compute/conda-spark-namespace:v4'

        rpc.add_containers(spark_master_container)

        kube.create_replication_controller(rpc, ns)
        import ipdb
        ipdb.set_trace()
        pass

        pod = Pod.from_jupyter_container(proxy, '')
        pod.add_ipyparallel_containers()
        kube.create_pod(pod)

        pod_name = pod.name
        created_pod = wait_for_running_pod(kube, pod_name)

        app_url = "{url}/".format(url=proxy.lookup(pod_name))
        print("JUPYTER APP URL:", app_url)
        self.write("Jupyter notebook running at: <a href=\"{0}\">{0}</a>".format(app_url))
        self.finish()
