# -*- coding: utf-8 -*-

from src import calculator as calc

delays = [
    (45, 0.022222),
    (14, 0.071429),
    (0, 0)
]


def test_should_compute_delay_per_request():
    for data in delays:
        actual = calc.delay_per_request(data[0])
    assert actual == data[1]


def test_should_compute_percentiles():
    data = [47.0, 49.0, 50.0, 48.8, 49.0, 49.0, 49.1, 49.1, 48.9, 48.9]
    actual = calc.percentiles(data)
    assert actual == "50%:47.081. 75%:47.1215. 90%:47.1458. 95%:47.1539. 100%:47.162. "
