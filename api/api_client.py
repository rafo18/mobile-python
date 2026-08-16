import requests


class ApiClient:

    def __init__(
        self,
        base_url,
        name="API"
    ):

        self.base_url = base_url
        self.name = name

        # =====================================================
        # EVIDENCIA DE LA ÚLTIMA OPERACIÓN
        # =====================================================

        self.last_method = None
        self.last_endpoint = None
        self.last_parameters = None
        self.last_status_code = None
        self.last_response = None

        # =====================================================
        # INDICA SI EXISTE UNA LLAMADA PENDIENTE DE EVIDENCIA
        # =====================================================

        self.has_evidence = False

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

        self.last_parameters = {

            "params":
                params or {},

            "headers":
                headers or {}
        }

        self.last_status_code = (
            response.status_code
        )

        try:

            self.last_response = (
                response.json()
            )

        except ValueError:

            self.last_response = (
                response.text
            )

        self.has_evidence = True

        return response

    # =========================================================
    # POST
    # =========================================================

    def post(
        self,
        endpoint,
        body=None,
        headers=None
    ):

        url = f"{self.base_url}{endpoint}"

        response = requests.post(
            url,
            json=body,
            headers=headers
        )

        # =====================================================
        # GUARDAR EVIDENCIA
        # =====================================================

        self.last_method = "POST"

        self.last_endpoint = url

        self.last_parameters = {

            "headers":
                headers or {},

            "body":
                body or {}
        }

        self.last_status_code = (
            response.status_code
        )

        try:

            self.last_response = (
                response.json()
            )

        except ValueError:

            self.last_response = (
                response.text
            )

        self.has_evidence = True

        return response

    # =========================================================
    # PUT
    # =========================================================

    def put(
        self,
        endpoint,
        body=None,
        headers=None
    ):

        url = f"{self.base_url}{endpoint}"

        response = requests.put(
            url,
            json=body,
            headers=headers
        )

        self.last_method = "PUT"

        self.last_endpoint = url

        self.last_parameters = {

            "headers":
                headers or {},

            "body":
                body or {}
        }

        self.last_status_code = (
            response.status_code
        )

        try:

            self.last_response = (
                response.json()
            )

        except ValueError:

            self.last_response = (
                response.text
            )

        self.has_evidence = True

        return response

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        endpoint,
        headers=None
    ):

        url = f"{self.base_url}{endpoint}"

        response = requests.delete(
            url,
            headers=headers
        )

        self.last_method = "DELETE"

        self.last_endpoint = url

        self.last_parameters = {

            "headers":
                headers or {}
        }

        self.last_status_code = (
            response.status_code
        )

        try:

            self.last_response = (
                response.json()
            )

        except ValueError:

            self.last_response = (
                response.text
            )

        self.has_evidence = True

        return response

    # =========================================================
    # OBTENER EVIDENCIA
    # =========================================================

    def get_last_evidence(self):

        return {

            "api":
                self.name,

            "method":
                self.last_method,

            "endpoint":
                self.last_endpoint,

            "parameters":
                self.last_parameters,

            "status_code":
                self.last_status_code,

            "response":
                self.last_response
        }

    # =========================================================
    # LIMPIAR EVIDENCIA
    # =========================================================

    def clear_last_evidence(self):

        self.last_method = None

        self.last_endpoint = None

        self.last_parameters = None

        self.last_status_code = None

        self.last_response = None

        self.has_evidence = False