from .swagger_client.models.v1_object_meta import V1ObjectMeta
from .swagger_client.models.v1_replication_controller import V1ReplicationController
from .swagger_client.models.v1_replication_controller_spec import V1ReplicationControllerSpec
from .swagger_client.models.v1_replication_controller_status import V1ReplicationControllerStatus
from .swagger_client.models.v1_pod_template_spec import V1PodTemplateSpec
from .swagger_client.models.v1_pod_spec import V1PodSpec


class ReplicationController(V1ReplicationController):

    def __init__(self, name, proxy=None, *args, **kwargs):
        super(ReplicationController, self).__init__(*args, **kwargs)
        self.kind = "ReplicationController"
        self.api_version = "v1"
        self.metadata = V1ObjectMeta()
        self.status = V1ReplicationControllerStatus()
        self.metadata.name = name

        self.spec = V1ReplicationControllerSpec()
        self.spec.replicas = 1
        # self.spec.ports = []

        self.spec.template = V1PodTemplateSpec()
        self.spec.template.metadata = V1ObjectMeta()
        self.spec.template.spec = V1PodSpec()
        self.spec.template.spec.containers = []

    def set_selector(self, name):
        """
        Set various component names
        :param name:
        :return:
        """
        self.spec.selector = {'component': name}
        self.spec.template.metadata.labels = {'component': name}

    def set_replicas(self, num):
        """
        :param num: int -- number of replicas
        :return: None
        """
        self.spec.replicas = num

    def add_containers(self, container):
        """
        :param container: ContainerTemplate
        :return: None
        """
        self.spec.template.spec.containers.append(container)

    def output_yaml(self):
        import yaml
        print(yaml.safe_dump(self.to_dict(), default_flow_style=False))

