from kubealerta.config.config import load_kube_config
from kubealerta.operator.nodenotify import main as nodenotify_main  # Renamed to avoid conflict
from kubernetes.client.rest import ApiException
import time

def main():
    try:
        # Load Kubernetes configuration
        load_kube_config()

        while True:
            print("Starting CRD processing...")
            nodenotify_main()  # Call the main function from nodenotify
            print("Sleeping for 100 seconds...")
            time.sleep(100)  # Sleep for 300 seconds before next iteration

    except ApiException as e:
        print(f"Error during execution: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
