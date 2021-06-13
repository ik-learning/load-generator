# -*- coding: utf-8 -*-

# how to use https://github.com/getsentry/responses
import responses

from src import request


@responses.activate
def test_should_make_post_request_ok():
    url = 'http://example.com/Live'
    responses.add(responses.POST,
                  'http://example.com/Live',
                  json={"successful": True}, status=200)
    actual = request.post(url)
    assert actual == 200
