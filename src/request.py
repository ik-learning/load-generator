# -*- coding: utf-8 -*-
import requests
import json
import time
import logging

from src.statistics import ResponseStatistics

logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

# error https://docs.python-requests.org/en/master/user/quickstart/#timeouts

# we should get requests_time from Statistics
payload = json.dumps({"name": "test", "date": "09:11:00", "requests_sent": 1})

headers = {"Accept": "*/*", "Content-Type": "application/json"}

FAILURE_EXCEPTIONS = (
    ConnectionError,
    ConnectionRefusedError,
    ConnectionResetError,
    Exception
)


def post(url, timeout=2):
    """
    Send an HTTP request, and catch any exception that might occur due to connection problems.
    """
    code = 500
    error = None
    start_time = time.perf_counter()
    try:
        # TODO: validate input
        response = requests.post(url=url, data=payload, headers=headers, timeout=timeout)
        # TODO: validate output
        code = response.status_code
    except FAILURE_EXCEPTIONS as e:
        logging.debug(e)
        error = True
    elapsed = time.perf_counter() - start_time

    # print(response)
    # print(response.json())
    return ResponseStatistics(code=code, execution_time=elapsed, error=error)
