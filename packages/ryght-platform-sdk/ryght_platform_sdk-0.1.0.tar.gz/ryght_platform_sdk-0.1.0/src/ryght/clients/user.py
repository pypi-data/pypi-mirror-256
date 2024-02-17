# <---| * Module Information |--->
# ==================================================================================================================== #
"""
    :param FileName     :   user.py
    :param Author       :   Sudo
    :param Date         :   2/02/2024
    :param Copyright    :   Copyright (c) 2024 Ryght, Inc. All Rights Reserved.
    :param License      :   # TODO
    :param Description  :   # TODO
"""
__author__ = 'Data engineering team'
__copyright__ = 'Copyright (c) 2024 Ryght, Inc. All Rights Reserved.'

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import uuid
import logging

from ryght.utils import FlowTypes

from ryght.configs import Credentials
from ryght.clients.api import ApiClient

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class RyghtClient:
    id: uuid.UUID = uuid.uuid4()
    api_client: ApiClient

    def __init__(self, user_credentials: dict, env_path: str):
        logger.info(f'Ryght client ID: {self.id}\n\n')
        self.api_client = ApiClient(env_path)
        if 'auth_token_url' not in user_credentials:
            user_credentials['auth_token_url'] = self.api_client.token_manager.credentials.auth_token_url
        self.api_client.token_manager.credentials = Credentials(**user_credentials)
        self.api_client.token_manager.get_new_token()

    def list_collections(self):
        return self.api_client.search_collections()

    def get_collection_by_id(self, collection_id: str):
        return self.api_client.get_collection_details(collection_id)

    def completions(
            self,
            input_str: str,
            collection_id: str,
            flow: FlowTypes = FlowTypes.SEARCH,
            search_limit: int = 5,
            completion_model_id: str = None,
            document_ids=None
    ):
        if document_ids is None:
            document_ids = []
        return self.api_client.perform_completions(
            input_str,
            collection_id,
            flow,
            search_limit,
            completion_model_id,
            document_ids
        )

    def list_models(self):
        return self.api_client.get_embedding_models()

    def get_model(self, model_id: str = None):
        return self.api_client.get_embedding_model_by_id(model_id)

# -------------------------------------------------------------------------------------------------------------------- #
