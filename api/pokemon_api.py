from api.base_api import BaseApi


class PokemonApi(BaseApi):

    def get_pokemon(
        self,
        pokemon
    ):

        return self.api_client.get(
            f"/pokemon/{pokemon}"
        )