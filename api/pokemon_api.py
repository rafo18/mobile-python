from api.endpoints import Endpoints


class PokemonApi:

    def __init__(self, client):
        self.client = client

    def get_pokemon(self, pokemon):

        return self.client.get(
            f"{Endpoints.POKEMON}/{pokemon}"
        )