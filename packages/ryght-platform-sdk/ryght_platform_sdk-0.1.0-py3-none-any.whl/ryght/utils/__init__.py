# <---| * Module Information |--->
# ==================================================================================================================== #
"""
    :param FileName     :   utils/__init__.py
    :param Author       :   Sudo
    :param Date         :   2/06/2024
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
import enum
import logging

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class RequestMethods(enum.Enum):
    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    PATCH = 'PATCH'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'


# -------------------------------------------------------------------------------------------------------------------- #

class FlowTypes(enum.Enum):
    SEARCH = 'SEARCH'
    REASON = 'REASON'
    DOCUMENT_REASON = 'DOCUMENT_REASON'
    SEARCH_AND_REASON = 'SEARCH_AND_REASON'
    MULTIPLE_DOCUMENT_REASON = 'MULTIPLE_DOCUMENT_REASON'
    REASON_SEARCH_AND_REASON = 'REASON_SEARCH_AND_REASON'


# -------------------------------------------------------------------------------------------------------------------- #
def set_logging_format(new_format):
    for handler in logging.root.handlers:
        handler.setFormatter(logging.Formatter(new_format))


def initialize_logging(file_path: str = '../logs/playground.logs'):
    default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    new_run_format = '%(message)s'

    logging.basicConfig(
        level=logging.INFO,
        format=default_format,
        filename=file_path
    )
    run_id = uuid.uuid4()

    set_logging_format(new_run_format)
    logging.info('\n\n# -------------------------------------------------------------------------------------- #')
    logging.info(f'# -------------> | NEW RUN >> ID: {run_id} | < ------------- #')
    logging.info('# -------------------------------------------------------------------------------------- #\n\n')
    set_logging_format(default_format)
    return logging.getLogger(__name__)
# -------------------------------------------------------------------------------------------------------------------- #
