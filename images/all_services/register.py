import os
import sys
import json
import requests

PROXY_REGISTER = os.environ.get("PROXY_REGISTER", None)
APP_ID = os.environ.get("APP_ID", None)
POD_IP = os.environ.get("POD_IP", None)
APP_PORT = os.environ.get("APP_PORT", 8080)
APP_PORT_1 = os.environ.get("APP_PORT_1", 8081)
APP_PORT_2 = os.environ.get("APP_PORT_2", 8082)
APP_PORT_3 = os.environ.get("APP_PORT_3", 8083)

if PROXY_REGISTER is None:
    print("Missing environment variable PROXY_REGISTER")
    sys.exit(1)

if APP_ID is None:
    print("Missing environment variable APP_ID")
    sys.exit(1)


for PORT in [APP_PORT, APP_PORT_1, APP_PORT_2, APP_PORT_3]:
    if int(PORT) != 8080:
        app_id_port = "{}/{}".format(APP_ID, PORT)
    else:
        app_id_port = APP_ID

    target_url = "http://{}:{}".format(POD_IP, PORT)
    body = {"target": target_url}
    url = "{register}/api/routes/{app_id}".format(register=PROXY_REGISTER, app_id=app_id_port)

    req = requests.Request("POST", url, data=json.dumps(body))
    prepped = req.prepare()
    session = requests.Session()
    ret = session.send(prepped)

    if ret.status_code == 201:
        print("Register OK: {}".format(url))
    else:
        print("Register failed:")
        print(ret.text)
        sys.exit(1)
