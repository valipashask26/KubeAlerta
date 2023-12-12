# kubealerta

kubealerta is a Kubernetes plugin/operator designed to streamline notifications to Teams channels based on filtered resources. Please note that the project is currently under construction, and we are actively working on enhancing its features.

> [!NOTE]  
> Currently, **kubealerta** is configured to send notifications specifically for nodes..

## Deployment

Follow these steps to deploy **kubealerta** in your Kubernetes cluster:

1. Download the manifest file from [here](https://github.com/valipashask26/KubeAlerta/blob/main/deploy/manifest/manifest.yaml).
2. Deploy the manifest file in your Kubernetes cluster using the following command:

 ```bash
   kubectl apply -f manifest.yaml
```
The manifest will create:

- **Namespace**
- **ServiceAccount**
- **ClusterRole**
- **ClusterRoleBinding**
- **Deployment**
- **CRDs**

Here, it will deploy 3 types of CRDs:

1. **Notify:**
   - To add Teams links, use the following example YAML:
     ```yaml
     apiVersion: kubealerta.io/v1
     kind: Notify
     metadata:
       name: example-notify
       namespace: kubealerta
       labels:
         test: kubealerta-01
     spec:
       webhookURL: "https://teams.webhook.url"
     ```

2. **NamespacedFilter:**
   - Specify the resources you want to get notified about (e.g., pod, deployment, daemonset). Follow the example YAML:
     ```yaml
     apiVersion: kubealerta.io/v1
     kind: NamespacedFilter
     metadata:
       name: filter2
       namespace: kubealerta
       labels:
         test: kubealerta-02
     spec:
       resource: Deployment
       rNames:
         - docker-dind-deployment
       namespaces:
         - sample
     ```

3. **ClusterFilter:**
   - Specify cluster-level resources you want to get notified about (e.g., Nodes). Follow the example YAML:
     ```yaml
     apiVersion: kubealerta.io/v1
     kind: ClusterFilter
     metadata:
       name: node-alert
       namespace: kubealerta
       labels:
         test: kubealerta-01
     spec:
       resource: Nodes
       nodesNames:
         - aks-agent1pool
     ```
  Within this configuration, you possess the option to specify either the individual **nodeName** or the **nodepool name**. However, it's important to note that in the ``spec.resource`` field, you must explicitly mention **"Nodes,"** even when intending to target nodes using the nodepool name as a prefix. In such cases, kubeAlerta will recognize the provided nodepool name as a **prefix** and subsequently retrieve events for all nodes sharing that specified prefix.


**NOTE:** 
- The `notify` CRD is mandatory to create.
- When creating a CRD with `clusterfilter` or `namespacedfilter`, the labels you use should match with the `notify` you are going to create. For example: 
  - If you have created a `namespacedfilter` (sample-01) with labels `app: nginx`, then use the same labels for the `notify` CRD (notify-01) to establish a connection.
  - Labels in sample-01 should not match with sample-02.
  - Create all the resources in "**kubealerta**" Namespace only.


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](https://github.com/valipashask26/KubeAlerta/blob/main/LICENSE) file for details...