from concurrent.futures import ThreadPoolExecutor
import asyncio
import time
from client import TornadoHttpClient
import random
import aiohttp


async def main():
    loop = asyncio.get_event_loop()
    start_time = time.perf_counter()
    tasks = []
    clients = []
    base_url = "http://localhost:6389"
    for i in range(50):
        client = TornadoHttpClient(base_url)
        clients.append(client)
    async with aiohttp.ClientSession():
        for i in range(10000):
            client = random.choice(clients)
            data_to_post = {"message": {'echo': f'bismeet {i}'}}
            task = loop.create_task(client.post("echo", data_to_post))
            tasks.append(task)
    total_time = time.perf_counter() - start_time
    await asyncio.gather(*tasks)

    print(f"Total execution time: {total_time:.2f} seconds")


asyncio.run(main())
