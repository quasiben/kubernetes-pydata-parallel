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

        self.api = swagger.ApivApi(self.client)

    def list_pods(self):
        return self.api.list_pod()

    def create_pod(self, pod, namespace="default"):
        self.api.create_namespaced_pod(pod, namespace=namespace)

    def get_pod(self, name, namespace="default"):
        return self.api.read_namespaced_pod(name=name, namespace=namespace)

    def get_service(self, name, namespace="default"):
        return self.api.read_namespaced_service(name=name, namespace=namespace)
