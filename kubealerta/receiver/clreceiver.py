# currently not using


from kubealerta.config.config import load_kube_config
from kubernetes import client, config
from kubernetes.client.rest import ApiException

def get_filtered_resources():
    # Load Kubernetes configuration
    load_kube_config()

    # Create Kubernetes API client
    api_client = client.ApiClient()

    # Get list of ClusterFilter and Notify resources across all namespaces
    custom_objects_api = client.CustomObjectsApi(api_client)

    # Specify the group/version for your CustomResourceDefinitions (CRDs)
    group = "kubealerta.io"
    version = "v1"
    cl_filters_kind = "clfilters"
    notifies_kind = "notifies"

    try:
        # Get ClusterFilter resources across all namespaces
        cl_filters = custom_objects_api.list_cluster_custom_object(group, version, cl_filters_kind)

        # Get Notify resources across all namespaces
        notifies = custom_objects_api.list_cluster_custom_object(group, version, notifies_kind)

        # Create a dictionary to store filtered resources based on labels
        filtered_resources = {}

        # Process ClusterFilter resources and filter by label
        for cl_filter_item in cl_filters['items']:
            label_selector = cl_filter_item['metadata']['labels']

            # Filter Notify resources based on the label from ClusterFilter
            filtered_notifies = [
                notify_item for notify_item in notifies['items'] if
                all(label in notify_item['metadata']['labels'].items() for label in label_selector.items())
            ]

            # Store the filtered resources in the dictionary only if there are matching notifies
            if filtered_notifies:
                # Assuming there is only one matching Notify for simplicity, you can adjust as needed
                matching_notify = filtered_notifies[0]
                common_label = next(iter(label_selector.keys()), None)  # Change this based on your label structure
                filtered_resources[common_label] = {
                    'Resource': cl_filter_item['spec']['resource'],
                    'NodeNames': ', '.join(cl_filter_item['spec']['nodesNames']),
                    'WebhookURL': matching_notify['spec']['webhookURL']
                }

        # Print information about the filtered resources
        print("Filtered Resources across all namespaces:")
        for common_label, details in filtered_resources.items():
            print(f"- Common Label: {common_label}")
            print(f"  - Resource: {details['Resource']}")
            print(f"  - Node Names: {details['NodeNames']}")
            print(f"  - Webhook URL: {details['WebhookURL']}")
    except ApiException as e:
        print(f"Error getting resources: {e}")

def get_node_events(node_name):
    # Load Kubernetes configuration
    load_kube_config()

    # Create Kubernetes API client
    api_client = client.ApiClient()

    # Create CoreV1Api instance for working with CoreV1 API (which includes Events)
    core_v1_api = client.CoreV1Api(api_client)

    try:
        # Get events for the specified node
        events = core_v1_api.list_event_for_all_namespaces(field_selector=f'involvedObject.name={node_name}')

        # Print information about the events
        print(f"Events for Node {node_name}:")
        for event in events.items:
            print(f"- Type: {event.type}, Reason: {event.reason}, Message: {event.message}")
    except ApiException as e:
        print(f"Error getting node events: {e}")

# Call the function if this module is executed directly
if __name__ == "__main__":
    # Get and print filtered resources across all namespaces
    filtered_resources = get_filtered_resources()

    # Get and print events for each node
    for node_info in filtered_resources.values():
        node_name = node_info['NodeNames'].split(', ')[0]  # Assuming node names are comma-separated
        get_node_events(node_name)
