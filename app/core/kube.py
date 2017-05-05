from . import swagger_client as swagger


class Kubernetes(object):

    def __init__(self, host, username=None, password=None, verify_ssl=True):
        swagger.Configuration().verify_ssl = False
        self.client = swagger.ApiClient(host)

        if username and password:
            swagger.Configuration().username = username
            swagger.Configuration().password = password
            auth_token = swagger.Configuration().get_basic_auth_token()
            self.client.default_headers["Authorization"] = auth_token
            self.client.default_headers["Content-Type"] = "application/json"

        self.api = swagger.DefaultApi(self.client)

    def list_pods(self, namespace=None):
        pods = self.api.list_pod()
        if namespace:
            return [ p for p in pods.items if p.metadata.namespace == namespace ]
        else:
            return pods.items

    def create_pod(self, pod, namespace="default"):
        self.api.create_namespaced_pod(pod, namespace=namespace)

    def get_pod(self, name, namespace="default"):
        return self.api.read_namespaced_pod(name=name, namespace=namespace)

    def get_service(self, name, namespace="default"):
        return self.api.read_namespaced_service(name=name, namespace=namespace)

    def create_namespace(self, ns):
        self.api.create_namespace(ns)

    def delete_namespace(self, ns):
        self.api.delete_namespaced_namespace(ns.v1delete, ns.name)

    def get_namespace(self, name):
        ns = [n for n in self.get_namespaces().items if n.metadata.name == name][0]
        return ns

    def get_namespaces(self):
        return self.api.list_namespaced_namespace()

    def create_service(self, serv, name):
        """

        :param serv:
        :param name: str
        :return:
        """
        return self.api.create_namespaced_service(serv, namespace=name)

    def create_replication_controller(self, rpc, name):
        """
        :param rpc:
        :param name: str
        :return:
        """
        return self.api.create_namespaced_replication_controller(rpc, namespace=name)
