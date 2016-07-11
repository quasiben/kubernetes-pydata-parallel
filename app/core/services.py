from .swagger_client.models.v1_object_meta import V1ObjectMeta
from .swagger_client.models.v1_service import V1Service
from .swagger_client.models.v1_service_spec import V1ServiceSpec
from .swagger_client.models.v1_service_port import V1ServicePort
from .swagger_client.models.v1_service_status import V1ServiceStatus


class Service(V1Service):

    def __init__(self, name, proxy=None, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        self.kind = "Service"
        self.api_version = "v1"
        self.metadata = V1ObjectMeta()
        self.status = V1ServiceStatus()
        self.metadata.name = name

        self.spec = V1ServiceSpec()
        self.spec.ports = []
        self.spec.selector = {'component': name}

    def add_port(self, port, target_port, name='default'):
        """
        :param port: int
        :param target_port: int
        :param name: str
        :return: None
        """

        port_ = V1ServicePort()
        port_.port = port
        port_.target_port = target_port
        port_.name = name
        self.spec.ports.append(port_)

