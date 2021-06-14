# -*- coding: utf-8 -*-
import logging
from src.statistics import AStatistics
import concurrent.futures

logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

CONTROLLER_THREADS = 2
MONITOR_INTERVAL = 1


class Simulation:

    def __init__(self, stats: AStatistics, request, url):
        self.stats = stats
        self.request = request
        self.url = url

    def make_post_requests(self, number: int):
        logging.debug(f'start: {number}')
        for _ in range(number):
            result = self.request.post(self.url)
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
