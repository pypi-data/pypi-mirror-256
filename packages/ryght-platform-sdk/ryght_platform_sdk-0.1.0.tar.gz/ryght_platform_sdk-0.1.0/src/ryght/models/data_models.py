"""
    :param FileName     :   data_models.py
    :param Author       :   Sudo
    :param Date         :   02/1/2024
    :param Copyright    :   Copyright (c) 2024 Ryght, Inc. All Rights Reserved.
    :param License      :   # TODO
    :param Description  :   # TODO
"""
from dataclasses import Field
# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
from typing import Any
from datetime import datetime, timedelta
from pydantic import BaseModel, ConfigDict, Extra, model_validator


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
class EmbeddingModel(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: str
    name: str
    provider: str
    tags: str | None
    description: str | None
    default: bool = False


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
            embedding_models.append(EmbeddingModel(**model_info))
        return embedding_models


# -------------------------------------------------------------------------------------------------------------------- #
class ApiEndpoints(BaseModel):
    model_config = ConfigDict(extra='ignore')

    models: str
    base_url: str
    completions: str
    upload_document: str
    models_by_operations: str
    document_collections: str
    search_document_collection: str
# -------------------------------------------------------------------------------------------------------------------- #
