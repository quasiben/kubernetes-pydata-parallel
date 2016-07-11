import json

import requests


class Proxy(object):

    def __init__(self, lookup_url, register_url):
        self.lookup_url = lookup_url
        self.register_url = register_url
        self.session = requests.Session()

    @classmethod
    def from_kubernetes(cls, kubernetes):
        # lookup_service = kubernetes.get_service("proxy-lookup")
        # lookup_ip = lookup_service.status.load_balancer.ingress[0].ip
        # lookup_url = "http://{}".format(lookup_ip)
        # hardcode lookup URL for our tutorial:
        lookup_url = "https://scipy2016-cluster.jupyter.org"
        register_service = kubernetes.get_service("proxy-register")
        register_ip = register_service.status.load_balancer.ingress[0].ip
        register_url = "http://{}".format(register_ip)
        return cls(lookup_url=lookup_url, register_url=register_url)

    def register(self, app_id, proxy_url):
        body = {"target": proxy_url}
        url = "{url}/api/routes/{app_id}".format(url=self.register_url, app_id=app_id)
        req = requests.Request("POST", url, data=json.dumps(body))
        prepped = req.prepare()
        return self.session.send(prepped)

    def get_routes(self):
        url = "{url}/api/routes".format(url=self.register_url)
        req = requests.Request("GET", url)
        prepped = req.prepare()
        return self.session.send(prepped).json()

    def get_app_ids(self):
        data = self.get_routes()
        app_ids = [route.strip("/") for route in data.keys()]
        return app_ids

    def app_id_exists(self, app_id):
        route = "/{}".format(app_id)
        return self.route_exists(route)

    def route_exists(self, route):
        return route in self.get_routes().keys()

    def delete_route(self, app_id):
        url = "{url}/api/routes/{app_id}".format(url=self.register_url, app_id=app_id)
        req = requests.Request("DELETE", url)
        prepped = req.prepare()
        return self.session.send(prepped)

    def delete_all(self):
        routes = self.get_routes()
        for route in routes:
            print(self.delete_route(route.strip("/")))

    def lookup(self, app_id):
        return "{url}/{app_id}".format(url=self.lookup_url, app_id=app_id)
