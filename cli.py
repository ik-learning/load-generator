#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import time
import argparse

from src import client, calculator as calc
from src.statistics import Statistics
from src.config import Config
from src.simulation import SimulationV2

logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)


def run(config, target_rps, delay_per_request, token):
    simulation_start_time = time.perf_counter()
    stats = Statistics(simulation_start_time)
    sm = SimulationV2(
        stats, client=client, url=f'{config.host}/{config.path}', schemas=cfg.schemas, auth=token
    )
    sm.run(requests_count=requests, delay_per_request=delay_per_request)
    stats.print_statistics(target_rps=target_rps)


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

    cfg = Config(args.config_file)

    requests = cfg.requests_count
    target_rps = cfg.rps
    logging.info(f'run simulation... against {cfg.host}/{cfg.path}')
    run(config=cfg, target_rps=target_rps, delay_per_request=calc.delay_per_request(target_rps), token=args.auth_token)
