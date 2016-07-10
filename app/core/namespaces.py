from .swagger_client.models.v1_object_meta import V1ObjectMeta
from .swagger_client.models.v1_namespace import V1Namespace
from .swagger_client.models.v1_namespace_spec import V1NamespaceSpec
from .swagger_client.models.v1_namespace_status import V1NamespaceStatus

from .swagger_client.models.v1_delete_options import V1DeleteOptions


class NameSpace(V1Namespace):

    def __init__(self, name, proxy=None, *args, **kwargs):
        super(NameSpace, self).__init__(*args, **kwargs)
        self.kind = "Namespace"
        self.api_version = "v1"
        self.metadata = V1ObjectMeta()
        self.status = V1NamespaceStatus()
        self.metadata.name = name
        self.metadata.labels = {'name': name}
        self.spec = V1NamespaceSpec()
        self._name = None
        self.name = name
        self.v1delete = V1DeleteOptions()
        self.proxy = proxy
