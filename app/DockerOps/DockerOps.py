import subprocess

class DockerOpsInterface:
    def __init__(self, region: str):
        self.__region = region

    def get_region(self) -> str:
        return self.__region

    def delete_image_tag(self, image_name: str, tag: str) -> str:
        pass

    def delete_repository(self, repo_name: str) -> str:
        pass

    def get_latest_tag(self, repo_name: str) -> str:
        pass

    def get_all_tags_sorted(self, repo_name: str) -> dict:
        return {}

    def keep_tags_retention(self, repo_name: str, num_of_tags: str) -> str:
        pass

    def get_login_details(self) -> dict:
        return {}

    def docker_build(self, image_name: str, tag: str) -> str:
        pass

    def do_docker_login(self) -> str:
        login_details = self.get_login_details()

        docker_login_cmd = 'docker login -u {} -p {} {}'.format(login_details['user'], login_details['password'], login_details['url'])
        
        result = subprocess.Popen(docker_login_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]

        return result

    def __ensure_repository_existence(self, image_name: str) -> bool:
        return False

    def create_docker_repository(self, repo_name: str) -> str:
        return ''

    def docker_push(self, image_name: str, image_tag: str) -> str:
        if(self.__ensure_repository_existence(image_name)):

            self.do_docker_login()

            repo_address = self.get_login_details()['url'].replace('https://','')

            cur_image_full_name = '{}:{}'.format(image_name, image_tag)

            new_full_image_details = '{}/{}:{}'.format(repo_address, image_name, image_tag)

            docker_tag_cmd = 'docker tag {} {}'.format(cur_image_full_name, new_full_image_details)

            docker_push_cmd = 'docker push {}'.format(new_full_image_details)

        result = subprocess.Popen(docker_tag_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]

        result = subprocess.Popen(docker_push_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]

        return result

    def healthcheck(self) -> dict:
        pass