import subprocess
from ..DockerOps import DockerOpsInterface

class GcpDockerOps(DockerOpsInterface):

    def __init__(self, region = 'us'):
        DockerOpsInterface.__init__(self, region)

    def get_login_details(self) -> dict:

        docker_pass = subprocess.Popen('gcloud auth print-access-token', shell=True, stdout=subprocess.PIPE).communicate()[0]

        return {
            'user': 'oauth2accesstoken',
            'password': '{}'.format(docker_pass),
            'url': 'https://{}.gcr.io'.format(self.__region)#should taken from ENV VAR = [gcr.io, us.gcr.io, eu.gcr.io, asia.gcr.io]
        }

    def healthcheck(self) -> dict:
        #check gcp registry
        return {
            'healthy': True
        }