# -*- coding: utf-8 -*-

import numpy as np
from typing import List

SINGLE_THREAD = 1
THREAD_MULTIPLIER = 1.4

PERCENTILES_TO_REPORT = [0.50, 0.75, 0.90, 0.95, 1.0]

ONE_SECOND = 1


def delay_per_request(rps) -> float:
    """
    Calculate delay in between requests

    :param rps: target rps
    :return delay in between requests
    """
    return round(ONE_SECOND / rps, 6) if rps > 0 else 0


def percentiles(data: List[float]) -> str:
    result = ""
    for p in PERCENTILES_TO_REPORT:
        percentage = int(p * 100)
        result += f"{percentage}%:{np.percentile(data, p)}. "
    return result
