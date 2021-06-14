# -*- coding: utf-8 -*-
import requests
import json
import time
import logging
from jsonschema import validate, ValidationError

from src.statistics import ResponseStatistics

logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

# we should get requests_time from Statistics
payload = {"name": "test", "date": "09:11:00", "requests_sent": 1}

headers = {"Accept": "*/*", "Content-Type": "application/json"}

FAILURE_EXCEPTIONS = (
    ConnectionError,
    ConnectionRefusedError,
    ConnectionResetError,
    Exception
)


# TODO: method does too much
# 1. validate input
# 2. make requests
# 3. validate response
# 4. Aggregate requests metrics
def post(url, schemas: dict, timeout=2):
    """
    Send an HTTP request, and catch any exception that might occur due to connection problems.
    :param url:  URL for the new `request` object.
    :param schemas: JSON schema dictionary
    :param timeout: http requests timeout
    :return: statistics object
    """
    code = 500
    error = False
    start_time = time.perf_counter()
    try:

        if 'post' in schemas:
            validate(instance=payload, schema=schemas.get('post'))

        response = requests.post(url=url, json=payload, headers=headers, timeout=timeout)
        code = response.status_code

        if code == 200 and code in schemas:
            validate(instance=response.json(), schema=schemas.get(code))

    except ValidationError as e:
        logging.error(e)
        error = True
    except FAILURE_EXCEPTIONS as e:
        logging.error(e)
        error = True

    elapsed = time.perf_counter() - start_time

    return ResponseStatistics(code=code, execution_time=elapsed, error=error)
