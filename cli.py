#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import math
import concurrent.futures

from src import request
from src.statistics import WarmUpStatistics, Statistics, AStatistics

logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

EXPECTED_RPS_NUMBER = 45
REQUESTS_COUNT = 500
WARMUP_REQUESTS_NUMBER = math.ceil(REQUESTS_COUNT * 0.05)
CONTROLLER_THREADS = 2
MONITOR_INTERVAL = 1
REQUEST_URL = "http://localhost:8080/Live"


# TODO: should not do more then X requests per second
def make_request(st: AStatistics, url: str, number: int):
    logging.debug(f'start: {number}')
    for _ in range(number):
        result = request.post(url)
        st.add(result)
    logging.debug(f'done: {number}')


def required_number_of_users(rps):
    """
    Calculate required number of users/threads, adds extra user/thread
    :param rps: current rps number
    :return: required number of threads
    """
    number_of_threads = 1
    if rps < EXPECTED_RPS_NUMBER:
        number_of_threads = math.ceil(EXPECTED_RPS_NUMBER / rps)
    return number_of_threads


def output_statistics(stats: Statistics, frequency=1):
    """
    output statistics
    :param stats:
    :param frequency: how often to execute statistics
    :return: output statistics data
    """
    # do not start thread right away
    time.sleep(frequency)
    while stats.request_count < REQUESTS_COUNT:
        rps = stats.current_rps()
        stats.add_rps(rps)
        logging.info(
            f'processing. Number of requests:{stats.request_count}. RPS:{rps}. Time:{stats.execution_time()}')
        time.sleep(frequency)
    logging.info('completed ...')
    logging.info(
        f'\tstatistics. Requests:{stats.request_count}. Time:{stats.execution_time()}. RPS:{stats.average_rps()}'
    )


if __name__ == "__main__":
    start_time = time.perf_counter()
    st = WarmUpStatistics(start_time)
    logging.info(f"warmup. warming up servers with {WARMUP_REQUESTS_NUMBER} requests")
    make_request(st, REQUEST_URL, WARMUP_REQUESTS_NUMBER)

    logging.info(
        f"warmup. number of requests {st.request_count}. {st.response_codes}. time: {st.execution_time()}"
    )
    users_count = required_number_of_users(st.current_rps())
    logging.info(
        f"warmup. average RPS for single thread {st.current_rps()}. required number of users: {users_count} "
        f"in order to achieve {EXPECTED_RPS_NUMBER} RPS"
    )
    logging.info("ready to run simulation")
    simulation_start_time = time.perf_counter()
    stats = Statistics(simulation_start_time)
    with concurrent.futures.ThreadPoolExecutor(max_workers=users_count + CONTROLLER_THREADS) as executor:
        for i in range(users_count):
            number_of_requests_per_thread = int(REQUESTS_COUNT / users_count)
            if i == 0:
                # (optional) first thread should make a bit more requests
                number_of_requests_per_thread += REQUESTS_COUNT % users_count
            executor.submit(make_request, stats, REQUEST_URL, number_of_requests_per_thread)
        # statistics thread
        executor.submit(output_statistics, stats, MONITOR_INTERVAL)
