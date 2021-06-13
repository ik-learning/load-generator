# -*- coding: utf-8 -*-

import math
import numpy as np
from typing import List

SINGLE_THREAD = 1

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
    return number_of_threads


def percentiles(data: List[float]) -> str:
    result = ''
    for p in PERCENTILES_TO_REPORT:
        result += f'{p}:{np.percentile(data, p)}. '
    return result
