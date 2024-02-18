# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
from pydantic_settings import BaseSettings, SettingsConfigDict


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class Credentials(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    username: str | None
    password: str | None
    client_id: str | None
    client_secret: str | None

    @staticmethod
    def init_none():
        return Credentials(**{
            'username': None,
            'password': None,
            'client_id': None,
            'client_secret': None
        })

# -------------------------------------------------------------------------------------------------------------------- #
