#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import time
import argparse

from src import request, calculator as calc, simulation as sm
from src.statistics import WarmUpStatistics, Statistics
from src.config import Config

logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config-file", help="configuration file", default="example.config.json"
    )
    parser.add_argument(
        "--auth-token",
        help="authentication token",
        default=os.environ.get("AUTH_TOKEN"),
    )
    args = parser.parse_args()

    start_time = time.perf_counter()
    cfg = Config(args.config_file)
    logging.info("warmup ...")
    logging.info(
        f"warmup. warming up {cfg.host} with {cfg.warmup_requests_count} requests"
    )

    stats = WarmUpStatistics(start_time)
    warmup_simulation = sm.Simulation(
        stats=stats,
        request=request,
        url=f"{cfg.host}/{cfg.path}",
        schemas=cfg.schemas,
        auth=args.auth_token,
    )
    warmup_simulation.make_post_requests(cfg.warmup_requests_count)

    logging.info(
        f"warmup. requests: {stats.request_count}. codes: {stats.response_codes}. time: {stats.execution_time()} "
        f"errors: {len(stats.errors)}"
    )
    users_count = calc.required_number_of_users(cfg.rps, stats.current_rps())
    logging.info(
        f"warmup. average RPS for single thread {stats.current_rps()}. required number of users: {users_count} "
        f"in order to hist target {cfg.rps} RPS"
    )
    logging.info("simulation ...")
    simulation_start_time = time.perf_counter()
    stats = Statistics(simulation_start_time)
    simulation = sm.Simulation(
        stats=stats,
        request=request,
        url=f"{cfg.host}/{cfg.path}",
        schemas=cfg.schemas,
        auth=args.auth_token,
    )
    simulation.run(users_count=users_count, requests_count=cfg.requests_count)

    logging.info("completed ...")
    logging.info(
        f"\tstatistics. Requests:{stats.request_count}. Time:{stats.execution_time()}"
        f"\n\t\t\t Average RPS:{stats.average_rps()}. Median RPS:{stats.median_rps()}. target RPS: {cfg.rps}"
        f"\n\t\t\t Percentiles {stats.quantiles()}."
    )
