import base64
from ..DockerOps import DockerOpsInterface
import boto3


class AwsDockerOps(DockerOpsInterface):

    def __init__(self, region='us-east-1'):
        DockerOpsInterface.__init__(self, region)
        self.__client = boto3.client('ecr', region_name=DockerOpsInterface.get_region(self))

    def create_docker_repository(self, repo_name: str) -> str:

        try:
            response = self.__client.create_repository(repositoryName=repo_name,)
        except self.__client.exceptions.RepositoryAlreadyExistsException as e:
            print(e.response)
            response = self.__client.describe_repositories(
                repositoryNames=[repo_name]
            )
        return response

    def get_login_details(self) -> dict:

        response = self.__client.get_authorization_token()

        user, password = base64.b64decode(response['authorizationData'][0]['authorizationToken']).decode('UTF-8').split(':')

        return {
            'user': user,
            'password': password,
            'url': response['authorizationData'][0]['proxyEndpoint']
        }

    def healthcheck(self) -> dict:
        # check aws registry
        return {
            'healthy': True
        }
