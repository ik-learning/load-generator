#!/usr/bin/env python3

import logging

from src import request

logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


def make_request(url, number):
    for i in range(number):
        result = request.post(url)


if __name__ == "__main__":
    make_request('http://localhost:8080/Live', 5)
    logging.info('completed')
