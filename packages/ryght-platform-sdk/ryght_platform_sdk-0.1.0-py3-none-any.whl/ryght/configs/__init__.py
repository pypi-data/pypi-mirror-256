# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import logging
from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class Credentials(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    username: str
    password: str
    client_id: str
    client_secret: str
    auth_token_url: str

# -------------------------------------------------------------------------------------------------------------------- #
