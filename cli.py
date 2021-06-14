#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import math


from src import request, calculator as calc, simulation as sm
from src.statistics import WarmUpStatistics, Statistics


logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

EXPECTED_RPS_NUMBER = 45
REQUESTS_COUNT = 500
WARMUP_REQUESTS_COUNT = math.ceil(REQUESTS_COUNT * 0.05)
REQUEST_URL = "http://localhost:8080/Live"


if __name__ == "__main__":
    start_time = time.perf_counter()

    logging.info(f"warmup. warming up servers with {WARMUP_REQUESTS_COUNT} requests")
    stats = WarmUpStatistics(start_time)
    warmup_simulation = sm.Simulation(stats=stats, request=request, url=REQUEST_URL)
    warmup_simulation.make_post_requests(WARMUP_REQUESTS_COUNT)

    logging.info(
        f"warmup. number of requests {stats.request_count}. {stats.response_codes}. time: {stats.execution_time()}"
    )
    users_count = calc.required_number_of_users(EXPECTED_RPS_NUMBER, stats.current_rps())
    logging.info(
        f"warmup. average RPS for single thread {stats.current_rps()}. required number of users: {users_count} "
        f"in order to achieve {EXPECTED_RPS_NUMBER} RPS"
    )
    logging.info("ready to run simulation")
    simulation_start_time = time.perf_counter()
    stats = Statistics(simulation_start_time)
    simulation = sm.Simulation(stats=stats, request=request, url=REQUEST_URL)
    simulation.run(users_count=users_count, requests_count=REQUESTS_COUNT)
