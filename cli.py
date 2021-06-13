#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import math
import concurrent.futures

from src import request, calculator as calc
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


if __name__ == "__main__":
    start_time = time.perf_counter()
    st = WarmUpStatistics(start_time)
    logging.info(f"warmup. warming up servers with {WARMUP_REQUESTS_NUMBER} requests")
    make_request(st, REQUEST_URL, WARMUP_REQUESTS_NUMBER)

    logging.info(
        f"warmup. number of requests {st.request_count}. {st.response_codes}. time: {st.execution_time()}"
    )
    users_count = calc.required_number_of_users(EXPECTED_RPS_NUMBER, st.current_rps())
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
                # (optional) first thread could make more requests, as number may not be divisible
                number_of_requests_per_thread += REQUESTS_COUNT % users_count
            executor.submit(make_request, stats, REQUEST_URL, number_of_requests_per_thread)
        # statistics thread
        executor.submit(stats.print_statistics, REQUESTS_COUNT, MONITOR_INTERVAL)
