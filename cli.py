#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import math


from src import request, calculator as calc, simulation as sm
from src.statistics import WarmUpStatistics, Statistics
from src.config import Config

logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

if __name__ == "__main__":
    start_time = time.perf_counter()

    # TODO: read from args
    cfg = Config('example.config.json')
    logging.info(f"warmup. warming up servers with {cfg.warmup_requests_count} requests")

    stats = WarmUpStatistics(start_time)
    warmup_simulation = sm.Simulation(stats=stats, request=request, url=f'{cfg.host}/{cfg.path}')
    warmup_simulation.make_post_requests(cfg.warmup_requests_count, schemas=cfg.schemas)

    logging.info(
        f"warmup. requests: {stats.request_count}. codes: {stats.response_codes}. time: {stats.execution_time()} "
        f'errors: {len(stats.errors)}'
    )
    users_count = calc.required_number_of_users(cfg.rps, stats.current_rps())
    logging.info(
        f"warmup. average RPS for single thread {stats.current_rps()}. required number of users: {users_count} "
        f"in order to achieve {cfg.rps} RPS"
    )
    logging.info("ready to run simulation")
    simulation_start_time = time.perf_counter()
    stats = Statistics(simulation_start_time)
    simulation = sm.Simulation(stats=stats, request=request, url=REQUEST_URL)
    simulation.run(users_count=users_count, requests_count=cfg.requests_count)
