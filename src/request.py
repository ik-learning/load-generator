# -*- coding: utf-8 -*-
import requests
import json

# error https://docs.python-requests.org/en/master/user/quickstart/#timeouts

# we should get requests_time from Statistics
payload = json.dumps({
    "name": "test",
    "date": "09:11:00",
    "requests_sent": 1
})

headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json'
}


def post(url, timeout=2):
    response = requests.post(url=url, data=payload, headers=headers, timeout=timeout)

    if response.status_code == 200:
        code = response.status_code
    else:
        code = response.status_code
    # print(response)
    # print(response.json())
    # return response.elapsed.microseconds
    return response.status_code
