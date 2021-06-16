# -*- coding: utf-8 -*-
import requests
import time
import logging

from src.statistics import ResponseStatistics

logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

headers = {"Accept": "*/*", "Content-Type": "application/json"}

FAILURE_EXCEPTIONS = (
    ConnectionError,
    ConnectionRefusedError,
    ConnectionResetError,
    Exception,
)


# 1. make requests
# 2. Setup authentication header
async def post(client, url: str, payload: dict, auth: str):
    code = 500
    start = time.perf_counter()
    try:

        if auth:
            headers["X-Api-Key"] = auth

        async with client.post(
            url,
            json=payload,
            headers=headers,
        ) as resp:
            code = resp.status
            data = await resp.json()

            return ResponseStatistics(
                code=code, execution_time=time.perf_counter() - start, error=False, data=data
            )
    except FAILURE_EXCEPTIONS as e:
        logging.error(e)
        error = True

    elapsed = time.perf_counter() - start
    return ResponseStatistics(code=code, execution_time=elapsed, error=error)
