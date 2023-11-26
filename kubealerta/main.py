# main.py
from config.config import load_kube_config
from operator.nodenotify import get_filtered_resources
from kubernetes.client.rest import ApiException

def main():
    try:
        # Load Kubernetes configuration from config.py
        load_kube_config()

        # Call the receiver function without specifying a namespace
        get_filtered_resources()

    except ApiException as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
