# -*- coding: utf-8 -*-

from src import config


def test_should_flatten_configuration():
    cfg = config.Config("fixtures/config.json")
    assert cfg.rps == 30
    assert cfg.requests_count == 50
