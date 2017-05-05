
import os

KUBERNETES_API = os.environ["KUBERNETES_API"]
KUBERNETES_USERNAME = os.environ.get("KUBERNETES_USERNAME", None)
KUBERNETES_PASSWORD = os.environ.get("KUBERNETES_PASSWORD", None)
LOCAL = bool(os.environ.get("LOCAL", False))
