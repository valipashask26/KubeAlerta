# currently not using
# nsreceiver.py
from kubealerta.config.config import load_kube_config
from kubernetes import client, config
from kubernetes.client.rest import ApiException

def get_filtered_resources(namespace=None):
    if not namespace:
        # Specify a default namespace or retrieve dynamically based on your logic
        namespace = "sk-admin"

    # Load Kubernetes configuration
    load_kube_config()

    # Create Kubernetes API client
    api_client = client.ApiClient()

    # Get list of NamespacedFilter and Notify resources in the specified namespace
    custom_objects_api = client.CustomObjectsApi(api_client)

    # Specify the group/version for your CustomResourceDefinitions (CRDs)
    group = "kubealerta.io"
    version = "v1"
    ns_filters_kind = "nsfilters"
    notifies_kind = "notifies"

    try:
        # Get NamespacedFilter resources
        ns_filters = custom_objects_api.list_namespaced_custom_object(group, version, namespace, ns_filters_kind)

        # Get Notify resources
        notifies = custom_objects_api.list_namespaced_custom_object(group, version, namespace, notifies_kind)

        # Create a dictionary to store filtered resources based on labels
        filtered_resources = {}

        # Process NamespacedFilter resources and filter by label
        for ns_filter_item in ns_filters['items']:
            label_selector = ns_filter_item['metadata']['labels']

            # Filter Notify resources based on the label from NamespacedFilter
            filtered_notifies = [notify_item for notify_item in notifies['items'] if
                                 label_selector.items() <= notify_item['metadata']['labels'].items()]

            # Store the filtered resources in the dictionary
            filtered_resources[ns_filter_item['metadata']['name']] = {
                'Resource': ns_filter_item['spec']['resource'],
                'ResourceName': ', '.join(ns_filter_item['spec']['rNames']),
                'Namespace': ns_filter_item['metadata']['namespace'],
                'WebhookURLs': [notify_item['spec']['webhookURL'] for notify_item in filtered_notifies]
            }

        # Print information about the filtered resources
        print(f"Filtered Resources in namespace {namespace}:")
        for ns_filter_name, details in filtered_resources.items():
            print(f"- NamespacedFilter: {ns_filter_name}")
            print(f"  - Resource: {details['Resource']}")
            print(f"  - Resource Names: {details['ResourceName']}")
            print(f"  - Namespace: {details['Namespace']}")
            print(f"  - Webhook URLs: {', '.join(details['WebhookURLs'])}")
    except ApiException as e:
        print(f"Error getting resources: {e}")

# Call the function if this module is executed directly
if __name__ == "__main__":
    # Get and print filtered resources with the default or dynamically obtained namespace
    get_filtered_resources()
