# -*- coding: utf-8 -*-

import time, logging
from typing import List, Dict
from abc import ABC, abstractmethod

from src import calculator

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(module)s %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)


class ResponseStatistics:
    def __init__(self, code, execution_time, error, data={}):
        self.code = code
        self.time = execution_time
        self.error = error
        self.data = data

    def __str__(self):
        return f'code:{self.code}. time:{self.time}'

    def __repr__(self):
        return self.__str__()


class AStatistics(ABC):
    def __init__(self, start_time, count):
        self.started = start_time
        self.request_count: int = count
        self.response_times: List[int] = list()
        # as for now we not really care what type of error
        self.errors: List = list()
        self.response_codes_stats: Dict[str, list] = dict()
        self.validation_errors: List[str] = []

    @abstractmethod
    def add(self, st: ResponseStatistics) -> None:
        pass

    def execution_time(self) -> float:
        return round(time.perf_counter() - self.started, 1)

    def current_rps(self) -> float:
        return round(self.request_count / self.execution_time(), 1)

    def validation_error(self, value: str):
        self.validation_errors.append(value)


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
        if st.error:
            self.errors.append(st.error)

        if st.code not in self.response_codes:
            self.response_codes[st.code] = 1
            self.response_codes_stats[st.code] = [st.time]
        else:
            self.response_codes[st.code] = self.response_codes[st.code] + 1
            stats = self.response_codes_stats[st.code]
            stats.append(st.time)


class Statistics(AStatistics):
    def __init__(self, start_time):
        super(Statistics, self).__init__(start_time, 0)
        self.response_codes: Dict[str, int] = dict()
        self.total_response_time = start_time

    def add(self, st: ResponseStatistics) -> None:
        """
        increase request count by one
        thread safe
        :return: None
        """
        self.request_count += 1
        self.response_times.append(st.time)
        self.total_response_time += st.time
        self.response_times.append(st.time)

        if st.error:
            self.errors.append(st.error)
        if st.code not in self.response_codes:
            self.response_codes[st.code] = 1
        else:
            self.response_codes[st.code] = self.response_codes[st.code] + 1

    # TODO: test
    # TODO: move into its own class
    def print_statistics(self, target_rps):
        """
        output statistics
        :param target_rps: target rps to achieve
        """
        logging.info(
            f"processing. Number of requests:{self.request_count}. "
            f'\n\taverage RPS:{self.average_rps()} and target RPS:{target_rps}'
            f"\n\texecution time:{self.execution_time()}"
            f'\n\tpercentiles:{self.quantiles()}'
            f'\n\tcodes:{self.response_codes}'
            f'\n\terrors:{len(self.errors)}'
        )

    def average_rps(self) -> float:
        return round(self.request_count / self.execution_time(), 1)

    def quantiles(self):
        return calculator.percentiles(sorted(self.response_times, reverse=True))

    def __str__(self):
        return f'\tcodes:{self.response_codes}. requests:{self.request_count}' \
               f'\n\terrors:{self.errors}'

    def __repr__(self):
        return self.__str__()
