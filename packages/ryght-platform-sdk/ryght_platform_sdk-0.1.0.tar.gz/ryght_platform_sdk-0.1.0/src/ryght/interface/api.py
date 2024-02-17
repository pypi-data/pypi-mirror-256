# <---| * Module Information |--->
# ==================================================================================================================== #
"""
    :param FileName     :   api.py
    :param Author       :   Sudo
    :param Date         :   2/07/2024
    :param Copyright    :   Copyright (c) 2024 Ryght, Inc. All Rights Reserved.
    :param License      :   # TODO
    :param Description  :   # TODO
"""
__author__ = 'Data engineering team'
__copyright__ = 'Copyright (c) 2024 Ryght, Inc. All Rights Reserved.'

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import time
import yaml
import logging
import importlib.util

from ryght.utils import RequestMethods

from ryght.configs import Credentials
from ryght.models.data_models import Token
from ryght.managers.tokens import TokenManager
from ryght.models.data_models import ApiEndpoints
from ryght.requests.http_requestor import HttpRequestExecutor

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class ApiInterface:
    credentials: Credentials
    api_endpoints: ApiEndpoints
    token_manager: TokenManager
    http_request_exec: HttpRequestExecutor

    def __init__(self, env_path: str):
        self.credentials = Credentials(_env_file=env_path)
        self.api_endpoints = self.load_api_endpoints()
        self.http_request_exec = HttpRequestExecutor()
        self.token_manager: TokenManager = TokenManager(
            token=Token.init_as_none(),
            credentials=self.credentials,
            requestor=self.http_request_exec
        )

    @staticmethod
    def load_api_endpoints(path_to_api_endpoints_yaml: str = None) -> ApiEndpoints:
        package_path = None
        if path_to_api_endpoints_yaml:
            package_path = path_to_api_endpoints_yaml
        else:
            package_name = 'ryght.configs'
            spec = importlib.util.find_spec(package_name)

            if spec is not None:
                package_path = spec.submodule_search_locations[0] + '/api_endpoints.yaml'
                logger.info(f"api_endpoints.yaml file found @ {package_path}")
            else:
                logger.error(f"api_endpoints.yaml file not found")

        with open(package_path, 'r') as file:
            endpoints = yaml.safe_load(file)['api_endpoints']
            return ApiEndpoints(**endpoints)

    @TokenManager.authenticate
    def execute_request(
            self,
            method: RequestMethods,
            url,
            headers,
            payload,
            **kwargs
    ) -> dict:

        request_fn = None  # placeholder for passing function
        try:
            if method == RequestMethods.GET:
                request_fn = self.http_request_exec.get
            elif method == RequestMethods.PUT:
                request_fn = self.http_request_exec.put
            elif method == RequestMethods.POST:
                request_fn = self.http_request_exec.post
            elif method == RequestMethods.PATCH:
                request_fn = self.http_request_exec.patch
            elif method == RequestMethods.DELETE:
                request_fn = self.http_request_exec.delete
            else:
                raise ValueError(f'Unknown method {method}')

            response = request_fn(url=url, headers=headers, data=payload, **kwargs)
            if response.status_code in [401, 403, 404]:
                logger.info(
                    f'Got client Error: {response.status_code}, Please check your credential & api endpoint variables'
                )
                response.raise_for_status()
            elif response.status_code in [500]:
                logger.info('Got client Error: 500, attempting new Token request after 5 seconds')
                time.sleep(5)
                response = request_fn(url=url, headers=headers, data=payload, **kwargs)
                response.raise_for_status()
        except ValueError as VE:
            logger.info(f'Value Error occurred: {VE}')
        except Exception as E:
            logger.info('Exception Occurred: {}'.format(E))
        else:
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f'Unknown Response status code: {response.status_code}')

# -------------------------------------------------------------------------------------------------------------------- #
