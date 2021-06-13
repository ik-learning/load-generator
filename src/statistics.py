# -*- coding: utf-8 -*-
import math
import time
from typing import List, Dict
from threading import Lock
from abc import ABC, abstractmethod


# todo validate json here?
class ResponseStatistics:
    def __init__(self, code, time):
        self.code = code
        self.time = time


class AStatistics(ABC):

    def __init__(self, start_time, count):
        self.started = start_time
        self.request_count: int = count
        self.response_times: List[int] = list()

    @abstractmethod
    def add(self, st: ResponseStatistics) -> None:
        pass

    def execution_time(self) -> float:
        return round(time.perf_counter() - self.started, 1)

    def current_rps(self) -> float:
        return round(self.request_count / self.execution_time(), 1)


class WarmUpStatistics(AStatistics):
    """
    Stores warmup load statistics.
    """

    def __init__(self, start_time):
        super(WarmUpStatistics, self).__init__(start_time, 0)
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


class Statistics(AStatistics):

    def __init__(self, start_time):
        super(Statistics, self).__init__(start_time, 0)
        self.response_codes: Dict[str, int] = dict()
        self.rps: List = list()
        self.total_response_time = 0
        self.lock: Lock = Lock()

    def add(self, st: ResponseStatistics) -> None:
        """
        increase request count by one
        :return: None
        """
        self.lock.acquire()
        self.request_count += 1

        self.response_times.append(st.time)
        self.total_response_time += st.time

        if st.code not in self.response_codes:
            self.response_codes[st.code] = 1
        else:
            self.response_codes[st.code] = self.response_codes[st.code] + 1
        self.lock.release()

    def add_rps(self, value) -> None:
        self.rps.append(value)

    # TODO: move into its own class
    def average_rps(self) -> int:
        return round(sum(self.rps) / len(self.rps), 1)
