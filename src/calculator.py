# -*- coding: utf-8 -*-

import math
import numpy as np
from typing import List

SINGLE_THREAD = 1
THREAD_MULTIPLIER = 1.4

PERCENTILES_TO_REPORT = [0.50, 0.75, 0.90, 0.95, 1.0]


def required_number_of_users(expected_rps, rps) -> int:
    """
    Calculate required number of users/threads, adds extra user/thread
    :param expected_rps: expected rps
    :param rps: current rps number
    :return: required number of threads
    """
    number_of_threads = SINGLE_THREAD
    if rps < expected_rps:
        number_of_threads = math.ceil(expected_rps / rps)
    return int(number_of_threads * THREAD_MULTIPLIER)


def percentiles(data: List[float]) -> str:
    result = ""
    for p in PERCENTILES_TO_REPORT:
        percentage = int(p * 100)
        result += f"{percentage}%:{np.percentile(data, p)}. "
    return result
