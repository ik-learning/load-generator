# -*- coding: utf-8 -*-

from src.statistics import WarmUpStatistics


def test_should_add_counter_increase():
    st = WarmUpStatistics()
    st.add()
    assert st.request_count == 1
