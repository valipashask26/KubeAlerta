# main.py
from kubealerta.config.config import load_kube_config
from kubealerta.operator.nodenotify import get_filtered_resources
from kubernetes.client.rest import ApiException
import time

def main():
    try:
        # Load Kubernetes configuration from config.py
        load_kube_config()

        while True:
            # Call the receiver function without specifying a namespace
            get_filtered_resources()

            # Sleep for 30 seconds
            time.sleep(30)

    except ApiException as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
