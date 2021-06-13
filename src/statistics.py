# -*- coding: utf-8 -*-

import time
from typing import List, Dict


# todo validate json here?
class ResponseStatistics:
    def __init__(self, code, time):
        self.code = code
        self.time = time


class WarmUpStatistics:
    """
    Stores warmup load statistics.
    """

    def __init__(self, start_time):
        self.started = start_time
        self.request_count: int = 0
        self.response_times: List[int] = list()
        self.response_codes: Dict[str, int] = dict()

    def add(self, st: ResponseStatistics) -> None:
        """
        increase request count by one
        :return: None
        """
        self.request_count += 1

        self.response_times.append(st.time)

        if st.code not in self.response_codes:
            self.response_codes[st.code] = 1
        else:
            self.response_codes[st.code] = self.response_codes[st.code] + 1

    def execution_time(self):
        return time.perf_counter() - self.started

    def current_rps(self):
        return round(self.request_count / self.execution_time(), 1)
