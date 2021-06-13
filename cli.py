#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import math
import concurrent.futures

from src import request
from src.statistics import WarmUpStatistics, Statistics

logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

WARMUP_REQUESTS_NUMBER = 5
EXPECTED_RPS_NUMBER = 30
REQUESTS_NUMBER = 500
CONTROLLER_THREADS = 2
REQUEST_URL = "http://localhost:8080/Live"


def make_request(stats: WarmUpStatistics, url: str, number: int):
    for i in range(number):
        # request number to add here as well
        result = request.post(url)
        stats.add(result)


def required_number_of_users(rps):
    """
    Calculate required number of users/threads, adds extra user/thread
    :param rps: current rps number
    :return: requred number of threads
    """
    extra_thread = 1
    if rps < EXPECTED_RPS_NUMBER:
        return math.ceil(EXPECTED_RPS_NUMBER / rps) + extra_thread
    else:
        # single thread is required
        return 1 + extra_thread


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
    stats = Statistics(start_time)
    with concurrent.futures.ThreadPoolExecutor(max_workers=users_count + CONTROLLER_THREADS) as executor:
        for i in range(users_count):
            executor.submit(make_request, stats, 'http://localhost:8080/Live', int(REQUESTS_NUMBER/users_count))
        executor.submit(make_request, stats, 'http://localhost:8080/Live', REQUESTS_NUMBER % users_count)
    print(time.perf_counter() - start_time)
    print(stats.request_count)
    print(len(stats.response_times))
