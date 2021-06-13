# -*- coding: utf-8 -*-

import time
from typing import List


class WarmUpStatistics:
    """
    Stores warmup load statistics.
    """

    def __init__(self):
        self.started = time.perf_counter()
        self.request_count: int = 0
        self.measures: List[int] = list()

    def add(self) -> None:
        """
        increase request count by one
        :return: None
        """
        self.request_count += 1
