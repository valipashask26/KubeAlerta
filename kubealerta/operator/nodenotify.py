from kubernetes import client, config, watch
import requests
import json
from datetime import datetime

# Load Kubernetes Config
# config.load_incluster_config()
config.load_incluster_config()
# Kubernetes API Client
custom_api = client.CustomObjectsApi()
v1 = client.CoreV1Api()

def list_crd_resources(group, version, plural):
    try:
        return custom_api.list_cluster_custom_object(group, version, plural)
    except client.exceptions.ApiException as e:
        print(f"Exception when calling CustomObjectsApi->list_cluster_custom_object: {e}")
        return None

# Custom JSON Encoder for datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def process_events(node_name_prefix, webhook_url):
    w = watch.Watch()
    try:
        for event in w.stream(v1.list_node):
            node_name = event['object'].metadata.name
            if node_name.startswith(node_name_prefix):
                print(f"Sending notification to {node_name}")
                # Convert the event object to a dictionary
                event_dict = event['object'].to_dict()

                # Prepare the payload with 'Summary' or 'Text'
                payload = {
                    "summary": f"Event for node {node_name}",
                    "text": json.dumps(event_dict, cls=DateTimeEncoder)
                }

                # Convert the payload to JSON
                payload_json = json.dumps(payload)

                # Send the JSON data to the webhook URL
                response = requests.post(webhook_url, data=payload_json, headers={'Content-Type': 'application/json'})
                if response.status_code != 200:
                    print(f"Failed to send notification for event on {node_name}")
                    print(f"HTTP Status Code: {response.status_code}")
                    print(f"Response Content: {response.content.decode()}")
                else:
                    print(f"Response sent successfully for event on {node_name}")
    except Exception as e:
        print(f"Error processing events: {e}")

def main():
    group = "kubealerta.io"
    version = "v1"
    cl_filters_kind = "clfilters"
    notifies_kind = "notifies"

    cl_filters = list_crd_resources(group, version, cl_filters_kind)
    notifies = list_crd_resources(group, version, notifies_kind)

    if cl_filters and notifies:
        for notify in notifies['items']:
            for cl_filter in cl_filters['items']:
                if notify['metadata']['labels'] == cl_filter['metadata']['labels']:
                    webhook_url = notify['spec']['webhookURL']
                    node_names = cl_filter['spec']['nodesNames']
                    print(f"Matched labels: Node names - {node_names}, Webhook URL - {webhook_url}")
                    for node_name in node_names:
                        process_events(node_name, webhook_url)

if __name__ == "__main__":
    main()
