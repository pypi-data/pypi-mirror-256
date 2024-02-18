"""
    :param FileName     :   test_data_models.py
    :param Author       :   Sudo
    :param Date         :   02/1/2024
    :param Copyright    :   Copyright (c) 2024 Ryght, Inc. All Rights Reserved.
    :param License      :   # TODO
    :param Description  :   # TODO
"""
import importlib.util
# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import yaml
import logging

from typing import Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, ConfigDict, model_validator, root_validator

# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class Token(BaseModel):
    """
    A data class that holds authorization token information
    """
    model_config = ConfigDict(extra='ignore')

    token_type: str | None
    expires_in: int | None
    access_token: str | None
    refresh_token: str | None
    refresh_expires_in: int | None
    token_expiry: datetime
    refresh_expiry: datetime

    @property
    def authorization_param(self) -> str:
        return (lambda: self.token_type + ' ' + self.access_token)()

    @staticmethod
    def init_as_none():
        return Token(
            **{
                'token_type': None,
                'expires_in': 5,
                'access_token': None,
                'refresh_token': None,
                'refresh_expires_in': 5
            }
        )

    @model_validator(mode='before')
    @classmethod
    def compute_expiration(cls, params: Any) -> Any:
        """

        :param params:
        :return:
        """
        assert 'expires_in' and 'refresh_expires_in' in params
        params['token_expiry'], params['refresh_expiry'] = Token.set_expiration(
            expires_in=params['expires_in'],
            refresh_expires_in=params['refresh_expires_in']
        )
        return params

    @staticmethod
    def set_expiration(expires_in: int, refresh_expires_in: int) -> tuple:
        """

        :param expires_in:
        :param refresh_expires_in:
        :return:
        """
        now = datetime.utcnow()
        return now + timedelta(seconds=expires_in), now + timedelta(seconds=refresh_expires_in)


# -------------------------------------------------------------------------------------------------------------------- #
class ApiEndpoints(BaseModel):
    model_config = ConfigDict(extra='ignore')

    models: str
    base_url: str
    documents: str
    completions: str
    auth_token_url: str
    upload_document: str
    models_by_operations: str
    document_collections: str
    search_document_collection: str
    search_default_collections: str

    @staticmethod
    def load_api_endpoints(path_to_api_endpoints_yaml: str = None):
        package_path = None
        if path_to_api_endpoints_yaml:
            package_path = path_to_api_endpoints_yaml
        else:
            package_name = 'ryght.configs'
            spec = importlib.util.find_spec(package_name)

            # Add dev / prod switch options
            if spec is not None:
                package_path = spec.submodule_search_locations[0] + '/api_endpoints.yaml'
                logger.debug(f"api_endpoints.yaml file found @ {package_path}")
            else:
                logger.error(f"api_endpoints.yaml file not found")

        with open(package_path, 'r') as file:
            endpoints = yaml.safe_load(file)['api_endpoints']
            return ApiEndpoints(**endpoints)


# -------------------------------------------------------------------------------------------------------------------- #

class Collection(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: str
    name: str
    tags: list
    states: list
    documents_count: int
    default: bool = False
    embedding_models: list

    @model_validator(mode='before')
    @classmethod
    def transform_data(cls, params: Any) -> Any:
        """

        :param params:
        :return:
        """
        if 'embeddingModels' in params:
            params['embedding_models'] = Collection.extract_embedding_models_details(params['embeddingModels'])
        if 'documentsCount' in params:
            params['documents_count'] = params['documentsCount']
        return params

    @staticmethod
    def extract_embedding_models_details(embedding_models_list: list) -> list:
        embedding_models = []
        for model_info in embedding_models_list:
            embedding_models.append(AIModels(**model_info))
        return embedding_models


# -------------------------------------------------------------------------------------------------------------------- #

class CompletionsResponse(BaseModel):
    model_config = ConfigDict(extra='ignore')

    answer: str | None
    embeddings: list | None

    @model_validator(mode='before')
    @classmethod
    def transform_data(cls, params: Any) -> Any:
        """

        :param params:
        :return:
        """
        if 'embeddings' not in params:
            params['embeddings'] = None
        if 'answer' not in params:
            params['answer'] = None
        return params

    @staticmethod
    def init_with_none():
        CompletionsResponse(**{'answer': None, 'embeddings': None})


# -------------------------------------------------------------------------------------------------------------------- #

class AIModels(BaseModel):
    model_config = ConfigDict(extra='allow')
    id: str
    name: str
    provider: str
    default: bool = False

    # Optional Fields
    tags: str | None
    description: str | None


# -------------------------------------------------------------------------------------------------------------------- #

class Documents(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: str
    name: str
    states: Optional[list[str]] = None
    content: Optional[str] = None

# -------------------------------------------------------------------------------------------------------------------- #
