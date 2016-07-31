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

    def __init__(self, proxy=None, add_pod_ip_env=True, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)
        self.name = "{name}"
        self.ports = []
        self.env = []
        if add_pod_ip_env:
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
        self.resources.requests = {"cpu": 0.5, "memory": "2Gi"}
        self.resources.limits = {"cpu": 2.0, "memory": "8Gi"}


class DaskSchedulerContainer(Container):

    def __init__(self, name, git_url='', *args, **kwargs):
        super(DaskSchedulerContainer, self).__init__(*args, **kwargs)
        self.name = name
        self.image = "gcr.io/computetesting/allservices:v15"
        self.command = ["/tmp/start-scheduler.sh"]
        self.add_port(8080)
        self.add_port(9000)
        self.add_port(9001)
        self.add_port(9002)
        self.add_port(7077)
        self.add_port(10000)
        self.add_env("APP_PORT", "8080")
        self.add_env("APP_PORT_1", "9000")
        self.add_env("APP_PORT_2", "9001")
        self.add_env("APP_PORT_3", "9002")
        self.add_env("APP_ID", name)
        self.add_env("GIT_URL", git_url)

    @classmethod
    def from_dask_scheduler(cls, proxy, git_url):
        proxy_name = gen_available_name(prefix="cluster", proxy=proxy)
        container = DaskSchedulerContainer(proxy_name, git_url, proxy=proxy, add_pod_ip_env=True)
        return container


class DaskWorkerContainer(Container):

    def __init__(self, name, *args, **kwargs):
        super(DaskWorkerContainer, self).__init__(*args, **kwargs)
        self.name = name
        self.image = "gcr.io/computetesting/allservices:v16"
        self.command = ["/tmp/start-worker.sh"]
        self.add_port(8081)

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
