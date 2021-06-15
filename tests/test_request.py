# -*- coding: utf-8 -*-

# how to use https://github.com/getsentry/responses
import responses

from src import request

payload = {"name": "", "date": "", "requests_sent": 0}

schemas = {
    "post": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "required": "true"},
            "date": {"type": "string"},
            "requests_sent": {"type": "number"},
        },
    }
}


@responses.activate
def test_should_make_post_request_ok():
    url = "http://example.com/Live"
    responses.add(
        responses.POST, "http://example.com/Live", json={"successful": True}, status=200
    )
    actual = request.post(url, payload=payload, schemas=schemas)
    assert actual.code == 200


@responses.activate
def test_should_make_post_request_500():
    url = "http://example.com/Live"
    responses.add(
        responses.POST, "http://example.com/Live", json={"successful": True}, status=200
    )
    actual = request.post(url, payload={}, schemas=schemas)
    assert actual.code == 500


@responses.activate
def test_should_make_post_request_ok_without_error():
    url = "http://example.com/Live"
    responses.add(responses.POST, "http://example.com/Live", body=Exception("..."))
    actual = request.post(url, payload, schemas)
    assert actual.error is True


@responses.activate
def test_should_handle_error():
    url = "http://example.com/Live"
    responses.add(
        responses.POST, "http://example.com/Live", json={"successful": True}, status=200
    )
    actual = request.post(url, payload, schemas)
    assert actual.error is False


@responses.activate
def test_should_success_without_schema_set():
    url = "http://example.com/Live"
    responses.add(
        responses.POST, "http://example.com/Live", json={"incorrect": True}, status=200
    )
    actual = request.post(url, payload, schemas=dict())
    assert actual.error is not True


@responses.activate
def test_should_validate_response_schema():
    url = "http://example.com/Live"
    responses.add(
        responses.POST, "http://example.com/Live", json={"incorrect": True}, status=200
    )
    actual = request.post(url, payload, schemas={})
    assert actual.error is False
