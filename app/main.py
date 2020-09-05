from flask import Flask,request,jsonify
import logging
import json
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

docker_ops = None
dns_ops = None
cloud_provider = os.environ['cloudProvider'] if os.environ.get('cloudProvider') is not None else 'AWS'
cloud_region = os.environ['cloudRegion'] if os.environ.get('cloudRegion') is not None else 'AWS'

if cloud_provider == 'AWS':
    from DockerOps.CloudProviders.aws import AwsDockerOps
    from DnsOps.CloudProviders.aws import AwsDnsOps
    docker_ops = AwsDockerOps()
    dns_ops = AwsDnsOps()
elif cloud_provider == 'Azure':
    from DockerOps.CloudProviders.azure import AzureDockerOps
    docker_ops = AzureDockerOps()
elif cloud_provider == 'GCP':
    from DockerOps.CloudProviders.gcp import GcpDockerOps
    docker_ops = GcpDockerOps()
elif cloud_provider == 'Alibaba':
    pass
else:
    from DockerOps.CloudProviders.aws import AwsDockerOps
    docker_ops = AwsDockerOps()

@app.route("/do_docker_login")
def docker_login():
    result = docker_ops.do_docker_login()
    return result

@app.route("/get_docker_login")
def get_docker_login():
    result = docker_ops.get_login_details()
    return jsonify(result)

@app.route("/create_docker_repository", methods=['POST'])
def create_docker_repository():
    req_data = request.get_json()

    repo_name = req_data['repo_name']

    result = docker_ops.create_docker_repository(repo_name)

    return result

@app.route("/docker_push", methods=['POST'])
def docker_push():
    req_data = request.get_json()

    image_name = req_data['image_name']
    image_tag = req_data['image_tag']

    result = docker_ops.docker_push(image_name, image_tag)

    return result

@app.route("/subdomain-record", methods=['PUT', 'POST', 'DELETE'])
def subdomain_record():
    req_data = request.get_json()
    result = dns_ops.subdomain_record(req_data['subdomain_name'], req_data['reference_fqdn'], 'A', request.method)
    return result

@app.route("/healthcheck")
def healthcheck():
    result = docker_ops.healthcheck()
    return jsonify(result)