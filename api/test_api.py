from api.base_api import BaseApi


class TestApi(BaseApi):

    def create_post(
        self,
        body,
        headers=None
    ):

        return self.api_client.post(
            "/posts",
            body=body,
            headers=headers
        )