# -*- coding: utf-8 -*-

# how to use https://github.com/getsentry/responses
import json
import pytest
from aiohttp import web

from src import client_interface as api

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


async def post_ok(request):
    if request.method == 'POST':
        request.app['value'] = (await request.post())['value']
        return web.Response(body={"successful": True}, status=200, )
    raise Exception('not supported')


@pytest.fixture
def client(loop, aiohttp_client):
    app = web.Application()
    app.router.add_post('/live', post_ok)
    return loop.run_until_complete(aiohttp_client(app))


async def test_should_make_post_request_failed(client):
    resp = await api.post(client, url='/live', payload={'value': 'foo'}, auth='')
    assert resp.code == 500
