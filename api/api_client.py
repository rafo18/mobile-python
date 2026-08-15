import requests


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None, headers=None):

        url = f"{self.base_url}{endpoint}"

        response = requests.get(
            url,
            params=params,
            headers=headers
        )

        return response