import requests


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None, headers=None):

        return requests.get(
            f"{self.base_url}{endpoint}",
            params=params,
            headers=headers
        )