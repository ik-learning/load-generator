#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import math

from src import request
from src.statistics import WarmUpStatistics

logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

WARMUP_REQUESTS_NUMBER = 5
EXPECTED_RPS_NUMBER = 30
REQUEST_URL = "http://localhost:8080/Live"


def make_request(stats: WarmUpStatistics, url: str, number: int):
    for i in range(number):
        result = request.post(url)
        stats.add(result)


def required_number_of_users(rps):
    if rps < EXPECTED_RPS_NUMBER:
        return math.ceil(EXPECTED_RPS_NUMBER / rps)
    else:
        # single thread is required
        return 1


if __name__ == "__main__":
    start_time = time.perf_counter()
    st = WarmUpStatistics(start_time)
    make_request(st, REQUEST_URL, WARMUP_REQUESTS_NUMBER)

    logging.info(
        f"completed. number of requests {st.request_count}. {st.response_codes}. time: {st.execution_time()}"
    )
    users_count = required_number_of_users(st.current_rps())
    logging.info(
        f"current RPS for single thread {st.current_rps()}. required number of users: {users_count}"
    )
