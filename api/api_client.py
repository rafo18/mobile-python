import requests


class ApiClient:

    def __init__(self, base_url):

        self.base_url = base_url

        # =====================================================
        # EVIDENCIA DE LA ÚLTIMA LLAMADA
        # =====================================================

        self.last_method = None
        self.last_endpoint = None
        self.last_parameters = None
        self.last_status_code = None
        self.last_response = None

    # =========================================================
    # GET
    # =========================================================

    def get(
        self,
        endpoint,
        params=None,
        headers=None
    ):

        url = f"{self.base_url}{endpoint}"

        response = requests.get(
            url,
            params=params,
            headers=headers
        )

        # =====================================================
        # GUARDAR EVIDENCIA
        # =====================================================

        self.last_method = "GET"

        self.last_endpoint = url

        self.last_parameters = params or {}

        self.last_status_code = response.status_code

        try:

            self.last_response = response.json()

        except ValueError:

            self.last_response = response.text

        return response