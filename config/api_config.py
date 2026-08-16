import os

from dotenv import load_dotenv


load_dotenv()


# =========================================================
# API BASE URLS
# =========================================================

POKEMON_API_URL = os.getenv(
    "POKEMON_API_URL"
)

TEST_API_URL = os.getenv(
    "TEST_API_URL"
)


# =========================================================
# API TIMEOUT
# =========================================================

API_TIMEOUT = int(
    os.getenv(
        "API_TIMEOUT",
        "30"
    )
)