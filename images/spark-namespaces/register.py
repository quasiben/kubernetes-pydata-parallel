import os
import sys
import json
import requests

PROXY_REGISTER = os.environ.get("PROXY_REGISTER", None)
APP_ID = os.environ.get("APP_ID", None)
POD_IP = os.environ.get("POD_IP", None)
APP_PORT = os.environ.get("APP_PORT", 8080)

if PROXY_REGISTER is None:
    print("Missing environment variable PROXY_REGISTER")
    sys.exit(1)

if APP_ID is None:
    print("Missing environment variable APP_ID")
    sys.exit(1)

target_url = "http://{}:{}".format(POD_IP, APP_PORT)
body = {"target": target_url}
url = "{register}/api/routes/{app_id}".format(register=PROXY_REGISTER, app_id=APP_ID)

req = requests.Request("POST", url, data=json.dumps(body))
prepped = req.prepare()
session = requests.Session()
ret = session.send(prepped)

if ret.status_code == 201:
    print("Register OK")
else:
    print("Register failed:")
    print(ret.text)
    sys.exit(1)
