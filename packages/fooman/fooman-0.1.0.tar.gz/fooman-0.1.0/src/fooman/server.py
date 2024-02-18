from .types import BrokerTypes
from .brokers import RedisBroker
from .broker import Broker
from .models import Request, Response
import pydantic


class RpcServer:
    def __init__(self, service_name: str):
        self._service_name = service_name
        self._handlers = {}

    def bind(self, handler):
        if handler.__name__ in self._handlers:
            raise KeyError(f"Handler {handler.__name__} already defined")

        self._handlers[handler.__name__] = pydantic.validate_call(
            handler,
            validate_return=True,
        )

        return handler
        
    async def start(self, connection_string: str, broker_type: str | BrokerTypes = BrokerTypes.REDIS):
        broker = self.broker = self._get_broker(broker_type)
        print(broker)
        await broker.connect(connection_string)
        await broker.consume(self._on_message, service_name=self._service_name, func_names=self._handlers.keys())


    async def _process_request(self, message) -> Request:
        print(message)
        return Request(**message)

    def _process_response(self, result) -> Response:
        return Response(result=result)

    async def _on_message(self, message) -> None:
        request = await self._process_request(message)
        response = self._process_response(await self._get_response(request))
        print(request)
        await self._reply_back(response, request.correlation_id)

    async def _get_response(self, request: Request):
        handler = self._handlers.get(request.method_name)
        result = await handler(**request.arguments)
        return result

    async def _reply_back(self, response: Response, correlation_id):
        await self.broker.produce(key=f"{correlation_id}", response=response.model_dump_json())

    def _get_broker(self, broker_type: str | BrokerTypes) -> Broker:
        broker_map = {BrokerTypes.REDIS: RedisBroker}
        broker_class = broker_map[BrokerTypes.from_string(broker_type) if not isinstance(broker_type, BrokerTypes) else broker_type]
        return broker_class()
