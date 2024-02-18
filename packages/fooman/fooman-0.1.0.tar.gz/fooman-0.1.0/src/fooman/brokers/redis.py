from ..broker import Broker
from typing import Callable
import redis
import json


class RedisBroker(Broker):

    async def connect(self, connection_string):
        parameters = dict()
        parameters["connection_pool"] = redis.asyncio.ConnectionPool.from_url(connection_string)
        self._connection = await redis.asyncio.StrictRedis(**parameters)

    async def disconnect(self):
        ...

    async def produce(self, key, response):
        await self._connection.rpush(key, response)

    async def get_replay(self, key):
        _, res = await self._connection.blpop(key, timeout=6)
        return res

    async def consume(self, func: Callable, service_name, func_names):
        while True:
            for func_name in func_names:
                service, req_data = await self._connection.blpop(f"{service_name}.{func_name}")
                print(req_data)
                await func(json.loads(req_data.decode()))
