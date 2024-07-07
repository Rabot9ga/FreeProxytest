import asyncio
import sys
import random
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from proxybroker import Broker
import aiohttp
from bs4 import BeautifulSoup
from logg import ColoredFormatter
import logging
from aiohttp_socks import ProxyConnector


async def show(proxies):
    lst = []
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        lst.append(f'{list(proxy.types.keys())[0].lower()}://{proxy.host}:{proxy.port}')
    return lst

async def get_url(lst_of_proxy):
    url = 'https://prodoctorov.ru/ufa/ergoterapevt/'
    type_con = 'socks5'
    login = 'avVUbUv1'
    passw = 'kRfNYvKR'
    proxy_url = '194.87.121.175'
    port = '64147'
    # connector = ProxyConnector.from_url(f'{type_con}://{login}:{passw}@{proxy_url}:{port}')
    for proxy in lst_of_proxy:
        try:
            logging.info(proxy)
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=proxy) as resp:
                    soup = BeautifulSoup(await resp.text(), 'html.parser')
                    print(soup.find('a', class_='b-header__logo-stat').text)
        except Exception as e:
            logging.error(e)

async def main():
    logging.basicConfig(level=logging.INFO,
                        handlers=[logging.StreamHandler()])
    logging.getLogger().handlers[0].setFormatter(ColoredFormatter())
    task = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], limit=20))
    lst_of_proxy = await show(proxies)
    while not task.done():
        await asyncio.sleep(1)
    await get_url(lst_of_proxy)

if __name__ == '__main__':
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    task1 = asyncio.gather(main())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(task1)
