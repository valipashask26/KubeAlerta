# config/config.py
from kubernetes import config

# def load_kube_config():
#     # Load Kubernetes configuration from the default kubeconfig file
#     config.load_kube_config()

def load_kube_config():
    # Load Kubernetes in-cluster configuration
    config.load_incluster_config()
