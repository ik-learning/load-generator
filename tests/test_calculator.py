# -*- coding: utf-8 -*-

from src import calculator as calc


def test_should_calculate_required_number_of_users():
    actual = calc.required_number_of_users(8789, 45)
    assert actual == 274


def test_should_calculate_percentiles():
    data = [47.0, 49.0, 50.0, 48.8, 49.0, 49.0, 49.1, 49.1, 48.9, 48.9]
    actual = calc.percentiles(data)
    assert actual == "50%:47.081. 75%:47.1215. 90%:47.1458. 95%:47.1539. 100%:47.162. "
