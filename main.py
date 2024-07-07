import asyncio
import sys
import random
import time

import aiohttp
from bs4 import BeautifulSoup
from logg import ColoredFormatter
import logging
import pandas as pd
from aiohttp_socks import ProxyConnector
from urllib.error import HTTPError


logging.basicConfig(level=logging.INFO,
                    handlers=[logging.StreamHandler()])
logging.getLogger().handlers[0].setFormatter(ColoredFormatter())


lst_of_correct_proxies = []

async def get_data_pro(proxy):
    global lst_of_correct_proxies
    url = 'https://prodoctorov.ru/ufa/ergoterapevt/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/126.0.0.0 Safari/537.36'}
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url, proxy=proxy, timeout=10, headers=headers) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                logging.info(f'Successfull proxy:  {proxy}')
                lst_of_correct_proxies.append(proxy)
    except:
        pass



async def main():
    global lst_of_correct_proxies
    lst_of_proxies = pd.read_csv('http.txt', header=None)[0].tolist()
    correct_proxies = list(map(lambda proxy: 'http://'+proxy, lst_of_proxies))
    await asyncio.gather(*(get_data_pro(proxy) for proxy in correct_proxies))
    print(lst_of_correct_proxies)
    print(len(lst_of_correct_proxies))

if __name__ == '__main__':
    asyncio.run(main())


# type_con = 'socks5'
# login = 'avVUbUv1'
# passw = 'kRfNYvKR'
# proxy_url = '194.87.121.175'
# port = '64147'
# # connector = ProxyConnector.from_url(f'{type_con}://{login}:{passw}@{proxy_url}:{port}')