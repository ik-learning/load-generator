# -*- coding: utf-8 -*-

from src import simulation as sim

from unittest.mock import MagicMock


def test_should_make_requests():
    expected = 34
    stats = MagicMock()
    request = MagicMock()
    sm = sim.Simulation(stats, request, 'https://example.com')
    sm.make_requests(expected)
    assert stats.add.call_count == expected
    assert request.post.call_count == expected
