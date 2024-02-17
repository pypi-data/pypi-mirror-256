import httpx


class Gitea:

    def __init__(self,
                 base_url: str,
                 user: str,
                 repo: str,
                 token: str
                 ):
        self.base_url = base_url
        self.base_api_url = f'{self.base_url}/api/v1'
        self.user = user
        self.repo = repo
        self.token = token
        self.headers = {
            'Authorization': f'token {self.token}'
        }

    def list_releases(self):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases'
        response = httpx.get(url, headers=self.headers)
        return response.json()

    def create_release(self,
                       title: str,  # 主标题
                       tag_name: str,  # 版本号
                       description: str,  # 描述
                       target_commitish: str = 'master',  # 目标提交
                       prerelease: bool = False,  # 是否为预发布
                       publish: bool = True  # 是否发布
                       ):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases'
        data = {
            'name': title,  # 主标题
            'target_commitish': target_commitish,
            'tag_name': tag_name,
            'body': description,
            'prerelease': prerelease,
            'draft': not publish  # 是否为草稿
        }
        response = httpx.post(url, headers=self.headers, json=data)
        return response.json()

    def get_releases_latest(self):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases/latest'
        response = httpx.get(url, headers=self.headers)
        return response.json()

    def get_releases_by_tag(self, tag_name: str):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases/tags/{tag_name}'
        response = httpx.get(url, headers=self.headers)
        return response.json()

    def delete_releases_by_tag(self, tag_name: str):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases/tags/{tag_name}'
        response = httpx.delete(url, headers=self.headers)
        return response.status_code

    def get_releases_by_id(self, id: int):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases/{id}'
        response = httpx.get(url, headers=self.headers)
        return response.json()

    def delete_releases_by_id(self, id: int):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases/{id}'
        response = httpx.delete(url, headers=self.headers)
        return response.status_code

    def update_releases_by_id(self,
                              id: int,
                              title: str = None,
                              tag_name: str = None,
                              description: str = None,
                              target_commitish: str = None,
                              prerelease: bool = None,
                              draft: bool = None,
                              ):
        old_data = self.get_releases_by_id(id)
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases/{id}'
        data = {
            'name': title or old_data.get('name'),  # 主标题
            'target_commitish': target_commitish or old_data.get('target_commitish'),
            'tag_name': tag_name or old_data.get('tag_name'),
            'body': description or old_data.get('body'),
            'prerelease': prerelease or old_data.get('prerelease'),
            'draft': draft or old_data.get('draft')  # 是否为草稿
        }
        response = httpx.patch(url, headers=self.headers, json=data)
        return response.json()

    def list_attachments_by_id(self, id: int):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases/{id}/assets'
        response = httpx.get(url, headers=self.headers)
        return response.json()

    def creat_releases_attachments_by_id(self,
                                         id: int,  # releases ID
                                         name: str,  # 附件名
                                         file_path: str  # 文件路径
                                         ):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases/{id}/assets'
        response = httpx.post(url, params={
            'name': name
        }, files={
            'attachment': open(file_path, 'rb')
        }, headers=self.headers)
        return response.json()

    def delete_releases_attachments_by_id(self, id: int, attachment_id: int):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases/{id}/assets/{attachment_id}'
        response = httpx.delete(url, headers=self.headers)
        return response.status_code

    def update_releases_attachments_by_id(self,
                                          id: int,  # releases ID
                                          attachment_id: int,  # 附件ID
                                          name: str,  # 附件名
                                          file_path: str  # 文件路径
                                          ):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/releases/{id}/assets/{attachment_id}'
        response = httpx.patch(url, params={
            'name': name
        }, files={
            'attachment': open(file_path, 'rb')
        }, headers=self.headers)
        return response.json()

    def list_tags(self, page: int = 1, limit: int = 10):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/tags'
        response = httpx.get(url, headers=self.headers, params={
            'page': max(page, 1),
            'limit': min(limit, 50)
        })
        return response.json()

    def creat_tag(self, tar_name: str, message: str = None, target: str = None):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/tags'
        response = httpx.post(url, headers=self.headers, json={
            'tag_name': tar_name,
            'target': target,
            'message': message
        })
        return response.json()

    def get_tag_by_tag_name(self, tag_name: str):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/tags/{tag_name}'
        response = httpx.get(url, headers=self.headers)
        return response.json()

    def delete_tag_by_tag_name(self, tag_name: str):
        url = f'{self.base_api_url}/repos/{self.user}/{self.repo}/tags/{tag_name}'
        response = httpx.delete(url, headers=self.headers)
        return response.json()
