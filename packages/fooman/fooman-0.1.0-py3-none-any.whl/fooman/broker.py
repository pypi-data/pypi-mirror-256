

class Broker:
    def __init__(self, *, connection=None, url=None, **parameters):
        ...

    async def connect(self):
        raise NotImplementedError

    async def disconnect(self):
        raise NotImplementedError

    async def produce(self):
        raise NotImplementedError

    async def consume(self):
        raise NotImplementedError

    async def declare_queue(self, queue_name):
        """Declare a queue on this broker.  This method must be
        idempotent.
        """
        raise NotImplementedError
