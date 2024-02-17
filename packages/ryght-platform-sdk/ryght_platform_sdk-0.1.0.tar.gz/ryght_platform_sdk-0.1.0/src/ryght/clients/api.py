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
import json
import logging
from urllib.parse import urljoin

from ryght.interface.api import ApiInterface
from ryght.models.data_models import Collection, EmbeddingModel
from ryght.utils import RequestMethods, FlowTypes

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class ApiClient(ApiInterface):
    def __init__(self, env_path: str):
        super().__init__(env_path)

    def get_headers(self):
        return {'Authorization': self.token_manager.token.authorization_param}

    # Document Collections
    def get_collection_page_by_page(self, param: dict = None):
        raise NotImplementedError(f'Perform completions not implemented')

    def search_collections(self, param: dict = None) -> dict[str, Collection]:
        logger.info(f'Getting available collections details')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.search_document_collection)
        logger.info(f'Requesting url: {url}')
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            headers=self.get_headers(),
            payload={},
            params=param
        )
        collections = {}
        if 'content' in result:
            for collection_details in result['content']:
                collections[collection_details['name']] = Collection(**collection_details)
        return collections

    def get_collection_details(self, collection_id: str) -> Collection:
        logger.info(f'Getting available collections details')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.document_collections)
        url = f'{url}/{collection_id}'
        logger.info(f'Collections by id: {collection_id}, fro, URL: {url}')
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            headers=self.get_headers(),
            payload={}
        )
        print(result)
        return Collection(**result)

    # Completions
    def perform_completions(
            self,
            input_str: str,
            collection_id: str | list,
            flow: FlowTypes = FlowTypes.SEARCH,
            search_limit: int = 5,
            completion_model_id: str = None,
            embedding_model_id: str = None,
            document_ids: list | None = None
    ):
        logger.info(f'Performing completions ... ')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.completions)
        payload = {
            "message": input_str,
            "flow": flow.value if isinstance(flow, FlowTypes) else None,
            "collectionId": collection_id,
            "completionModelId": completion_model_id,
            "limit": search_limit,
            "documentIds": document_ids
        }
        headers = self.get_headers()
        headers['Content-Type'] = 'application/json'
        result = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            payload=json.dumps(payload)
        )
        return result

    # Models
    def get_embedding_models(self):
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.models)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            headers=self.get_headers(),
            payload={}
        )
        models = []
        for model in result:
            models.append(EmbeddingModel(**model))
        return models

    def get_embedding_model_by_id(self, model_id: str):
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.models)
        url = f"{url}/{model_id}"
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            headers=self.get_headers(),
            payload={}
        )
        return EmbeddingModel(**result)

    def get_embedding_model_by_operations(self, operations: str = ""):
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.models_by_operations)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            headers=self.get_headers(),
            payload=json.dumps({
                "operation": operations
            })
        )
        models = []
        for model in result:
            models.append(EmbeddingModel(**model))
        return models

    # Documents
    def upload_documents(self, documents_path: str, file_name: str, file_format: str = '.pdf'):
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.upload_document)
        headers = self.get_headers()
        headers['Content-Type'] = 'application/json'
        data = {
            "file": "placeholder",
            "fileName": file_name + file_format,
            "tagIds": []
        }
        with open(documents_path + file_name + file_format, 'rb') as file:
            data['file'] = file

        result = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            payload=data
        )
        print(result)
        return result

    def search_documents(self):
        pass

    def rename_document(self):
        pass

    def get_document_by_id(self, document_id: str):
        pass

    def delete_document_by_id(self, document_id: str):
        pass

    # Notes
    def search_notes(self, filter_params: dict = None):
        pass

    def get_note_by_id(self, note_id: str):
        pass

    def create_note(self):
        pass

    def update_note(self):
        pass

# -------------------------------------------------------------------------------------------------------------------- #
