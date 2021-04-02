"""A DigitalOcean Python Pulumi program"""

import pulumi
import pulumi_digitalocean as do


CLUSTER_NAME = "k8s-learning"
NODE_SIZE = "s-2vcpu-4gb" #https://developers.digitalocean.com/documentation/changelog/api-v2/new-size-slugs-for-droplet-plan-changes/
NODE_COUNT = 2


cluster = do.KubernetesCluster(CLUSTER_NAME,
    region="nyc1",
    version="1.20.2-do.0",
    node_pool=do.KubernetesClusterNodePoolArgs(
        name="backend-pool",
        size=NODE_SIZE,
        node_count=NODE_COUNT,
        tags=["backend"],
        labels={
            "service": "backend",
            "priority": "high",
        }
    ))

pulumi.export("kubeconfig", cluster.kube_configs[0]["rawConfig"])


