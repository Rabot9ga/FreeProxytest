import asyncio
import sys
import random
import time

import requests
import aiohttp
from bs4 import BeautifulSoup
from logg import ColoredFormatter
import logging
import pandas as pd
from aiohttp_socks import ProxyConnector
from urllib.error import HTTPError
from models import get_amount_of_pages

logging.basicConfig(level=logging.INFO,
                    handlers=[logging.StreamHandler()])
logging.getLogger().handlers[0].setFormatter(ColoredFormatter())

lst_of_correct_proxies = []


async def get_working_proxies_lst(proxy):
    global lst_of_correct_proxies
    url = 'https://prodoctorov.ru/ufa/ergoterapevt/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/126.0.0.0 Safari/537.36'}
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url, proxy=proxy, timeout=10, headers=headers) as response:
                await response.text()
                logging.info(f'Successfull proxy:  {proxy}')
                lst_of_correct_proxies.append(proxy)
    except:
        pass


async def get_data():
    global lst_of_correct_proxies
    url = 'https://prodoctorov.ru/ufa/ergoterapevt/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/126.0.0.0 Safari/537.36'}
    logging.info(len(lst_of_correct_proxies))
    if len(lst_of_correct_proxies) == 0:
        await correct_proxies()
    else:
        proxy = random.choice(lst_of_correct_proxies)
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(url, proxy=proxy, timeout=10, headers=headers) as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    logging.critical(soup.title.text)

        except:
            lst_of_correct_proxies.remove(proxy)





async def correct_proxies():
    response = requests.get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt')
    with open('http.txt', 'wb') as f:
        f.write(response.content)
    proxies = list(map(lambda proxy: 'http://' + proxy, pd.read_csv('http.txt', header=None)[0].tolist()))
    await asyncio.gather(*(get_working_proxies_lst(proxy) for proxy in proxies))


async def main():
    global lst_of_correct_proxies
    await correct_proxies()
    # while True:
    #     await get_data()
    number_of_pages = get_amount_of_pages('https://prodoctorov.ru/cheboksary/pediatr/', lst_of_correct_proxies)
    print(number_of_pages)


if __name__ == '__main__':
    asyncio.run(main())

# type_con = 'socks5'
# login = 'avVUbUv1'
# passw = 'kRfNYvKR'
# proxy_url = '194.87.121.175'
# port = '64147'
# # connector = ProxyConnector.from_url(f'{type_con}://{login}:{passw}@{proxy_url}:{port}')
