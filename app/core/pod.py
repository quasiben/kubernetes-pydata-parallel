from .swagger_client.models.v1_pod import V1Pod
from .swagger_client.models.v1_pod_spec import V1PodSpec
from .swagger_client.models.v1_object_meta import V1ObjectMeta
from .swagger_client.models.v1_container import V1Container
from .swagger_client.models.v1_container_port import V1ContainerPort
from .swagger_client.models.v1_env_var import V1EnvVar
from .swagger_client.models.v1_env_var_source import V1EnvVarSource
from .swagger_client.models.v1_object_field_selector import V1ObjectFieldSelector
from .swagger_client.models.v1_resource_requirements import V1ResourceRequirements


class Container(V1Container):

    def __init__(self, proxy=None, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)
        self.name = "{name}"
        self.ports = []
        self.env = []
        self.add_pod_ip_env()

        self.proxy = proxy
        if self.proxy:
            self.add_proxy_register_env()

        self.add_default_resources()

    def add_port(self, port):
        port_ = V1ContainerPort()
        port_.container_port = port
        self.ports.append(port_)

    def add_env(self, name, value):
        env_ = V1EnvVar()
        env_.name = name
        env_.value = value
        self.env.append(env_)

    def add_pod_ip_env(self):
        env_ = V1EnvVar()
        env_.name = "POD_IP"
        field_selector = V1ObjectFieldSelector()
        field_selector.field_path = "status.podIP"
        env_source = V1EnvVarSource()
        env_source.field_ref = field_selector
        env_.value_from = env_source
        self.env.append(env_)

    def add_proxy_register_env(self):
        self.add_env("PROXY_REGISTER", self.proxy.register_url)

    def add_default_resources(self):
        self.resources = V1ResourceRequirements()
        self.resources.requests = {"cpu": 0.5, "memory": "1Gi"}
        self.resources.limits = {"cpu": 0.5, "memory": "1Gi"}


class JupyterContainer(Container):

    def __init__(self, name, git_url, *args, **kwargs):
        super(JupyterContainer, self).__init__(*args, **kwargs)
        self.name = name
        self.image = "gcr.io/continuum-compute/notebook:v1"
        self.command = ["/tmp/startup.sh"]
        self.add_port(8080)
        self.add_env("APP_ID", name)
        self.add_env("GIT_URL", git_url)


class SparkMasterContainer(Container):

    def __init__(self, name, *args, **kwargs):
        super(SparkMasterContainer, self).__init__(*args, **kwargs)
        self.name = name
        self.image = "gcr.io/continuum-compute/spark:v1"
        self.command = ["/tmp/start-spark-master.sh"]
        self.add_port(7077)


class SparkWorkerContainer(Container):

    def __init__(self, name, *args, **kwargs):
        super(SparkWorkerContainer, self).__init__(*args, **kwargs)
        self.name = name
        self.image = "gcr.io/continuum-compute/spark:v1"
        self.command = ["/tmp/start-spark-worker.sh"]


class DaskSchedulerContainer(Container):

    def __init__(self, name, *args, **kwargs):
        super(DaskSchedulerContainer, self).__init__(*args, **kwargs)
        self.name = name
        self.image = "gcr.io/continuum-compute/distributed:v1"
        self.command = ["/tmp/start-scheduler.sh"]
        self.add_port(9000)


class DaskWorkerContainer(Container):

    def __init__(self, name, *args, **kwargs):
        super(DaskWorkerContainer, self).__init__(*args, **kwargs)
        self.name = name
        self.image = "gcr.io/continuum-compute/distributed:v1"
        self.command = ["/tmp/start-worker.sh"]


def random_id(n=6):
    """
    Random integer of size N
    """
    from random import randint
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def gen_available_name(prefix, proxy):
    app_id = "{prefix}-{app_id}".format(prefix=prefix, app_id=random_id())
    if proxy.app_id_exists(app_id):
        return gen_available_name(prefix, proxy)
    return app_id


class Pod(V1Pod):

    def __init__(self, name, proxy=None, *args, **kwargs):
        super(Pod, self).__init__(*args, **kwargs)
        self.kind = "Pod"
        self.api_version = "v1"
        self.metadata = V1ObjectMeta()
        self.metadata.name = None
        self.metadata.labels = {}
        self.spec = V1PodSpec()
        self.spec.containers = []

        self._name = None
        self.name = name

        self.proxy = proxy

    @classmethod
    def from_jupyter_container(cls, proxy, git_url):
        pod_name = gen_available_name(prefix="jupyter", proxy=proxy)
        pod = cls(pod_name, proxy=proxy)
        container = JupyterContainer(pod_name, git_url, proxy=proxy)
        pod.spec.containers.append(container)
        return pod

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.metadata.name = self._name
        self.add_label("name", name)

    def add_label(self, name, value):
        self.metadata.labels.update({name: value})

    def add_container(self, container):
        self.spec.containers.append(container)

    def add_spark_containers(self):
        spark_master = SparkMasterContainer(self.name + "-spark-master")
        self.add_container(spark_master)
        spark_worker_1 = SparkWorkerContainer(self.name + "-spark-worker-1")
        self.add_container(spark_worker_1)
        spark_worker_2 = SparkWorkerContainer(self.name + "-spark-worker-2")
        self.add_container(spark_worker_2)

    def add_dask_containers(self):
        dask_scheduler = DaskSchedulerContainer(self.name + "-dask-master")
        self.add_container(dask_scheduler)
        dask_worker_1 = DaskWorkerContainer(self.name + "-dask-worker-1")
        self.add_container(dask_worker_1)
        dask_worker_2 = DaskWorkerContainer(self.name + "-dask-worker-2")
        self.add_container(dask_worker_2)

    def add_ipyparallel_containers(self):
        pass
