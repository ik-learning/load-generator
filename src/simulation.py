# -*- coding: utf-8 -*-
import datetime
import logging
import threading
import asyncio
import aiohttp

from src.statistics import AStatistics
from jsonschema import validate, ValidationError

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(module)s %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)

CONTROLLER_THREADS = 2
MONITOR_INTERVAL = 1

payload = {"name": "", "date": "", "requests_sent": 0}


class SimulationV2:

    def __init__(self, stats: AStatistics, client, url: str, schemas: dict, auth: str):
        self.stats = stats
        self.client = client
        self.url = url
        self.schemas = schemas
        self.auth = auth

    async def make_post_requests(self, client, name: str, number: int):
        payload["date"] = str(datetime.datetime.utcnow())
        payload["name"] = name
        payload["requests_sent"] = number

        try:

            if "post" in self.schemas:
                validate(instance=payload, schema=self.schemas.get("post"))

            result = await self.client.post(client=client, url=self.url, payload=payload, auth=self.auth)

            if result.code == 200 and result.code in self.schemas:
                validate(instance=result.data, schema=self.schemas.get(result.code))

        except ValidationError as e:
            logging.error(e)
            self.stats.validation_error(e.message)

        self.stats.add(result)
        return result

    async def _wrap(self, number: int, sleep: float):
        name = threading.currentThread().getName().lower()
        tasks = []
        async with aiohttp.ClientSession() as client:
            for n in range(number):
                task = asyncio.ensure_future(self.make_post_requests(client, name, n))
                tasks.append(task)
                await asyncio.sleep(sleep)
            responses = asyncio.gather(*tasks)
            await responses

    def run(self, requests_count, delay_per_request):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._wrap(requests_count, delay_per_request))
