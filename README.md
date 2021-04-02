# Pulumi Digital Ocean Kubernetes + Linkerd

[![Update Infra](https://github.com/RafaelFigueiredo/pulumi-kubernetes/actions/workflows/push.yaml/badge.svg)](https://github.com/RafaelFigueiredo/pulumi-kubernetes/actions/workflows/push.yaml)


This project is a basic pipeline to create a Kubernetes cluster on DigitalOcean


## Features
* Create a cluster defined by code, using [Pulumi](https://pulumi.com).
* kubectl config credentials are saved encrypted using Ansible-Vault
* Deploy Linkerd service mesh
* Pull request preview of modifications

## Sample code
```python
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
```
## How to use?

1. Create the following secrets in Settings > Secrets

    | Secret              | Description       |
    |---------------------|----------------------|
    | `ANSIBLE_VAULT_KEY`   | String used to encrypt/decrypt sensible artifacts. I suggest that you generate a random string using `openssl rand -base64 100`|
    | `DIGITALOCEAN_TOKEN`  | PAT(Personal Access Token) for DigitalOcean. Used by Pulumi to create resources. https://cloud.digitalocean.com/account/api/tokens |
    | `PULUMI_ACCESS_TOKEN` | Your Pulumi access token |   

2. Go to https://cloud.digitalocean.com to created resources
3. After setup your local environment, run `linkerd viz dashboard` and take a look in http://localhost:50750/grafana



## References
* https://docs.ansible.com/ansible/latest/cli/ansible-vault.html
* https://www.pulumi.com/docs/guides/continuous-delivery/github-actions/
* https://linkerd.io/