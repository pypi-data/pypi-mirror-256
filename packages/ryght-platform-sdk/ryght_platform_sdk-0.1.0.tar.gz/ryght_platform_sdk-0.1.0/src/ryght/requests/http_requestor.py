import asyncio
import aiohttp
import functools
import logging

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
class HttpRequestExecutor:
    def __init__(self):
        self.session = requests.Session()

    @staticmethod
    def handle_errors(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                response = func(self, *args, **kwargs)
                return response
            except RequestException as e:
                logger.info(f"HTTP request failed: {e}")
            except ValueError:
                logger.info("Invalid JSON response")

        return wrapper

    @handle_errors
    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    @handle_errors
    def post(self, url, data=None, **kwargs):
        return self.session.post(url, data=data, **kwargs)

    @handle_errors
    def put(self, url, data=None, **kwargs):
        return self.session.put(url, data=data, **kwargs)

    @handle_errors
    def patch(self, url, **kwargs):
        return self.session.patch(url, **kwargs)

    @handle_errors
    def delete(self, url, **kwargs):
        return self.session.delete(url, **kwargs)

    def close(self):
        logger.info('Closing requests Session ...')
        self.session.close()
        logger.info('Session closed...')

    def __del__(self):
        self.close()

# -------------------------------------------------------------------------------------------------------------------- #
