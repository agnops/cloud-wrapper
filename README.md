# cloud-wrapper

* local run:
```
#AWS
docker run -v /home/<USER>/.aws/config:/root/.aws/config -v /home/<USER>/.aws/credentials:/root/.aws/credentials -p 5000:5000 --name cloud-wrapper agnops/cloud-wrapper:aws

#GCP
docker run -v /home/<USER>/.boto:/root/.boto -e cloudProvider=GCP -p 5000:5000 --name cloud-wrapper agnops/cloud-wrapper:gcp

#Azure
docker run -v /home/<USER>/.boto:/root/.boto -e cloudProvider=Azure -e username=<user> -e password=<passwprd> -e tenant=<tenant> -p 5000:5000 --name cloud-wrapper agnops/cloud-wrapper:azure
```

## Installation

## * General prerequisites:
```
kubectl create namespace ci-cd-tools
```

## * Prerequisites for each cloud provider:
#### AWS:
```
kubectl create secret generic aws-account-config --from-file path/to/config  -n ci-cd-tools --dry-run -o yaml | kubectl apply -f -
kubectl create secret generic aws-account-credentials --from-file path/to/credentials  -n ci-cd-tools --dry-run -o yaml | kubectl apply -f -
```
#### Azure:
```
kubectl create secret generic azure-account-credentials --from-literal=username='<user>' --from-literal=password='<passwprd>' --from-literal=tenant='<tenant>' -n ci-cd-tools --dry-run -o yaml | kubectl apply -f -
```
#### GCP:
```
kubectl create secret generic gcp-config --from-file path/to/.boto  -n ci-cd-tools --dry-run -o yaml | kubectl apply -f -
```
#### Alibaba:
```
```

#### TODO:

1. Add DockerOps support for Alibaba Cloud.
2. Add DnsOps support for Azure, GCP and Alibaba Cloud
3. Docker image tag versioning - Until then, pullPolicy = Always.
4. Azure: list all tags in docker repo: `az acr repository show-tags --name fffff --repository bbb`