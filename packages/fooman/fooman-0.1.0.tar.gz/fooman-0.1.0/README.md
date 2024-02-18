<h1 align="center">
  <br>
  <a href="https://amirbahador-hub.github.io/fooman/"><img src="https://raw.githubusercontent.com/amirbahador-hub/fooman/main/logo.png" alt="FooMan" width="200"></a>
</h1>

<h4 align="center">Introducing an advanced, high-performance async RPC library designed specifically for seamless communication between microservices. Our cutting-edge solution offers robust support for popular message brokers such as Redis, Kafka, and RabbitMQ. Streamline your microservices architecture and unlock the full potential of distributed systems with our feature-rich library. Experience lightning-fast communication and effortless scalability, empowering your applications to deliver exceptional performance in today's demanding environments.</h4>

<p align="center">
  <a href="https://img.shields.io/badge/test-pass-green">
    <img src="https://img.shields.io/badge/test-pass-brightgreen"
         alt="TestBadge">
  </a>
  <a href="https://img.shields.io/badge/python-3.10-blue">
    <img src="https://img.shields.io/badge/python-3.10-blue"
         alt="PythonVersionBadge">
  </a>


</p>


<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
</p>

## Installation
```bash
pip install fooman
```

## Usage
server:
```python
from fooman import RpcServer
import asyncio

server = RpcServer("SomeService")

@server.bind
async def add(a, b):
    return a+b

async def main():
    await server.start("redis://localhost:6379")

asyncio.run(main())
```
client:
```python
from fooman import RpcClient
import asyncio

client = RpcClient("MyClient", "redis://localhost:6379")


async def main():
    anwer = await client.add(a=2,b=7)
    print(anwer)
    
asyncio.run(main())
```
