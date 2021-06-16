# -*- coding: utf-8 -*-

import datetime, time
import concurrent.futures
import unittest

from freezegun import freeze_time
from src.statistics import WarmUpStatistics, ResponseStatistics, Statistics

HTTP_OK = 200
AVERAGE_TIME_MILLISECONDS = 254


def test_should_add_counter_increase():
    rst = ResponseStatistics(HTTP_OK, AVERAGE_TIME_MILLISECONDS, error=False)
    st = WarmUpStatistics(None)
    st.add(rst)
    assert st.request_count == 1


def test_should_retrieve_execution_time():
    initial_datetime = datetime.datetime(
        year=2021, month=6, day=13, hour=10, minute=6, second=3, microsecond=0
    )
    with freeze_time(initial_datetime) as delorean:
        rst = ResponseStatistics(HTTP_OK, AVERAGE_TIME_MILLISECONDS, False)
        st = WarmUpStatistics(time.perf_counter())
        st.add(rst)
        delorean.tick(delta=datetime.timedelta(microseconds=AVERAGE_TIME_MILLISECONDS))
        assert st.execution_time() < 3


@freeze_time("2021-06-13 11:21:34")
def test_should_compute_rps():
    expected_requests = 10
    response_times = [
        0.05,
        0.234,
        0.123,
        0.789,
        0.021,
        0.612,
        0.207,
        0.021,
        0.112,
        0.345,
    ]
    st = WarmUpStatistics(time.perf_counter())
    for i in range(expected_requests):
        execution_time = response_times[i]
        time.sleep(execution_time)
        st.add(ResponseStatistics(HTTP_OK, execution_time, error=False))

    assert st.request_count == expected_requests
    assert round(st.current_rps(), 0) == 4


def under_tests(stats: Statistics, number: int):
    response_times = [
        0.05,
        0.234,
        0.123,
        0.789,
        0.021,
        0.612,
        0.207,
        0.021,
        0.112,
        0.345,
    ]
    for i in range(number):
        # request number to add here as well
        result = ResponseStatistics(
            code=200, execution_time=response_times * 100, error=False
        )
        stats.add(result)


@unittest.skip("should use async as it simpler")
def test_should_update_statistics_in_threaded_environment():
    workers = 2
    expected_numbers = 10
    st = Statistics(time.perf_counter())
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for i in range(workers):
            executor.submit(under_tests, st, expected_numbers)
    assert st.request_count != expected_numbers
