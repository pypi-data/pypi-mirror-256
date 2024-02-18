from fooman.brokers.redis import RedisBroker
import asyncio


async def main():
    broker = RedisBroker()
    broker.connect("redis://localhost:6379")
    await broker.produce("name", "amir")
    await broker.consume("name")

asyncio.run(main())