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

# we should get requests_time from Statistics
payload = {"name": "", "date": "", "requests_sent": 0}


class Simulation:

    def __init__(self, stats: AStatistics, request, url: str, schemas: dict):
        self.stats = stats
        self.request = request
        self.url = url
        self.schemas = schemas

    def make_post_requests(self, number: int):
        logging.debug(f'start: {number}')
        for _ in range(number):
            
            payload['date'] = str(datetime.datetime.utcnow())
            payload['name'] = threading.currentThread().getName().lower()
            payload['requests_sent'] = number

            result = self.request.post(self.url, payload=payload, schemas=self.schemas)
            self.stats.add(result)
        logging.debug(f'done: {number}')

    def run(self, users_count, requests_count):
        with concurrent.futures.ThreadPoolExecutor(max_workers=users_count + CONTROLLER_THREADS) as executor:
            for i in range(users_count):
                number_of_requests_per_thread = int(requests_count / users_count)
                if i == 0:
                    # (optional) first thread could make more requests, as number may not be divisible
                    number_of_requests_per_thread += requests_count % users_count
                executor.submit(self.make_post_requests, number_of_requests_per_thread)
            # statistics thread
            executor.submit(self.stats.print_statistics, requests_count, MONITOR_INTERVAL)
