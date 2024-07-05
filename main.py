import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from proxybroker import Broker
import aiohttp
from bs4 import BeautifulSoup


async def show(proxies):
    lst = []
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        print(f'{proxy.host}')
        lst.append(f'{list(proxy.types.keys())[0].lower()}://{proxy.host}:{proxy.port}')
    return lst

async def get_url():
    url = 'https://myip.ru/'
    task = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], limit=5))
    a = await show(proxies)
    while not task.done():
        await asyncio.sleep(1)
    print(a)
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url, proxy=proxy) as resp:
    #         soup = BeautifulSoup(await resp.text(), 'html.parser')
    #         print(soup.prettify())


if __name__ == '__main__':
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    task1 = asyncio.gather(get_url())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(task1)
