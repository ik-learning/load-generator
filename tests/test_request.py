# -*- coding: utf-8 -*-

# how to use https://github.com/getsentry/responses
import responses

from src import request


@responses.activate
def test_should_make_post_request_ok():
    url = "http://example.com/Live"
    responses.add(
        responses.POST, "http://example.com/Live", json={"successful": True}, status=200
    )
    actual = request.post(url)
    assert actual.code == 200


@responses.activate
def test_should_make_post_request_ok_without_error():
    url = "http://example.com/Live"
    responses.add(
        responses.POST, "http://example.com/Live", body=Exception('...')
    )
    actual = request.post(url)
    assert actual.error is True


@responses.activate
def test_should_handle_error():
    url = "http://example.com/Live"
    responses.add(
        responses.POST, "http://example.com/Live", json={"successful": True}, status=200
    )
    actual = request.post(url)
    assert actual.error is None
