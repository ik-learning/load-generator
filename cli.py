#!/usr/bin/env python3

import logging

from src import request
from src.statistics import WarmUpStatistics

logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


def make_request(stats: WarmUpStatistics, url: str, number: int):
    for i in range(number):
        result = request.post(url)
        stats.add()


if __name__ == "__main__":
    st = WarmUpStatistics()
    make_request(st, 'http://localhost:8080/Live', 5)
    logging.info(f'completed. number of requests {st.request_count}')
