import subprocess
import json
from ..DockerOps import DockerOpsInterface

class AzureDockerOps(DockerOpsInterface):

    def __init__(self, region = 'eastus'):
        DockerOpsInterface.__init__(self, region)
        self.__az_login()
        self.__resource_group = 'myResourceGroup'
        self.__registry_name = 'fffff'#must be unique - have to validate before initialize

    def __az_login(self):
        import os
        result = ''

        if((os.environ.get('username') is not None) and (os.environ.get('password') is not None) and (os.environ.get('tenant') is not None)):
            username = os.environ['username']
            password = os.environ['password']
            tenant = os.environ['tenant']

            az_login_cmd = 'az login --service-principal -u {} -p {} --tenant {}'.format(username, password, tenant)
                
            result = subprocess.Popen(az_login_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]

        return result

    def __init_acr(self):
        try:
            resource_group_cmd = 'az group create --name {} --location {}'.format(self.__resource_group, self.__region)
            
            result = subprocess.Popen(resource_group_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
            print(result)

            acr_create_cmd = 'az acr create --resource-group {} --name {} --admin-enabled true --sku Basic'.format(self.__resource_group, self.__registry_name)
            
            result = subprocess.Popen(acr_create_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
            print(result)
            return True
        except:
            return False

    def __ensure_repository_existence(self, image_name: str) -> bool:

        if(self.__init_acr()):
            return True
        return False

    def get_login_details(self) -> dict:

        get_docker_cred_cmd = 'az acr credential show --resource-group {} --name {}'.format(self.__resource_group, self.__registry_name)

        result = subprocess.Popen(get_docker_cred_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]

        acr_cred_obj = json.loads(result)

        acr_create_cmd = 'az acr create --resource-group {} --name {} --admin-enabled true --sku Basic'.format(self.__resource_group, self.__registry_name)
            
        result = subprocess.Popen(acr_create_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]

        registry_details = json.loads(result)

        return {
            'user': acr_cred_obj['username'],
            'password': acr_cred_obj['passwords'][0]['value'],
            'url': registry_details['loginServer']
        }

    def healthcheck(self) -> dict:
        #check aws registry
        return {
            'healthy': True
        }