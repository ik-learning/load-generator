# -*- coding: utf-8 -*-

import time, logging
from typing import List, Dict
from threading import Lock
from abc import ABC, abstractmethod
import statistics

from src import calculator

logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


class ResponseStatistics:

    def __init__(self, code, execution_time, error):
        self.code = code
        self.time = execution_time
        self.error = error


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
        not a thread safe
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
        # as for now we not really care what type of error
        self.errors: List = list()

    def add(self, st: ResponseStatistics) -> None:
        """
        increase request count by one
        thread safe
        :return: None
        """
        self.lock.acquire()

        self.request_count += 1
        self.response_times.append(st.time)
        self.total_response_time += st.time

        if st.error is True:
            self.errors.append(st.error)

        if st.code not in self.response_codes:
            self.response_codes[st.code] = 1
        else:
            self.response_codes[st.code] = self.response_codes[st.code] + 1

        self.lock.release()

    def add_rps(self, value) -> None:
        self.rps.append(value)

    # TODO: test
    # TODO: move into its own class
    def print_statistics(self, total_count, frequency=1):
        """
        output statistics
        :param total_count: total request count
        :param frequency: how often to execute statistics
        :return: output statistics data
        """
        # do not start thread right after away
        time.sleep(frequency)
        while self.request_count < total_count:
            rps = self.current_rps()
            self.add_rps(rps)
            logging.info(
                f'processing. Number of requests:{self.request_count}. RPS:{rps}. Time:{self.execution_time()}')
            time.sleep(frequency)
        logging.info('completed ...')
        logging.info(
            f'\tstatistics. Requests:{self.request_count}. Time:{self.execution_time()}'
            f'\n\t\t\t Average RPS:{self.average_rps()}. Median RPS:{self.median_rps()}. Mean RPS: {self.mean_rps()}'
            f'\n\t\t\t Percentiles {self.quantiles()}.'
        )

    # TODO: move into its own class
    def average_rps(self) -> int:
        return round(sum(self.rps) / len(self.rps), 1)

    # TODO: test
    # TODO: move into its own class
    def median_rps(self) -> int:
        return round(statistics.median(self.rps), 1)

    def mean_rps(self) -> int:
        return round(statistics.mean(self.rps), 1)

    def quantiles(self):
        return calculator.percentiles(sorted(self.rps, reverse=True))
