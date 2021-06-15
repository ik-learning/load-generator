# -*- coding: utf-8 -*-
import datetime
import logging
import threading

from src.statistics import AStatistics
import concurrent.futures

logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

CONTROLLER_THREADS = 2
MONITOR_INTERVAL = 1

payload = {"name": "", "date": "", "requests_sent": 0}


class Simulation:
    def __init__(self, stats: AStatistics, request, url: str, schemas: dict, auth: str):
        self.stats = stats
        self.request = request
        self.url = url
        self.schemas = schemas
        self.auth = auth

    def make_post_requests(self, number: int):
        name = threading.currentThread().getName().lower()
        logging.debug(f"start: {name}:{number}")
        for _ in range(number):

            # TODO: extract, dummy value object?
            payload["date"] = str(datetime.datetime.utcnow())
            payload["name"] = name
            payload["requests_sent"] = number

            result = self.request.post(
                self.url, payload=payload, schemas=self.schemas, auth=self.auth
            )
            self.stats.add(result)
        logging.debug(f"done: {name}:{number}")

    def run(self, users_count, requests_count):
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=users_count + CONTROLLER_THREADS
        ) as executor:
            for i in range(users_count):
                number_of_requests_per_thread = int(requests_count / users_count)
                if i == 0:
                    # (optional) first thread could make more requests, as number may not be divisible
                    number_of_requests_per_thread += requests_count % users_count
                executor.submit(self.make_post_requests, number_of_requests_per_thread)
            # statistics thread
            executor.submit(
                self.stats.print_statistics, requests_count, MONITOR_INTERVAL
            )
