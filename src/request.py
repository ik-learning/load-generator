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

# TODO: read from file
schema_post = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "date": {"type": "string"},
        "requests_sent": {"type": "number"}
    }
}

schema_200 = {
    "type": "object",
    "properties": {
        "successful": {"type": "bool"},
    }
}


def post(url, schemas=dict(), timeout=2):
    """
    Send an HTTP request, and catch any exception that might occur due to connection problems.
    :param url:
    :param schemas:
    :param timeout:
    :return: statistics object
    """
    code = 500
    error = False
    start_time = time.perf_counter()
    try:
        # TODO: test
        validate(instance=payload, schema=schema_post)
        response = requests.post(url=url, json=payload, headers=headers, timeout=timeout)
        code = response.status_code
        # TODO: test
        if code == 200:
            validate(instance=response.json(), schema=schema_200)
    except ValidationError:
        error = True
    except FAILURE_EXCEPTIONS as e:
        logging.debug(e)
        error = True
    elapsed = time.perf_counter() - start_time

    return ResponseStatistics(code=code, execution_time=elapsed, error=error)
