import requests
import random
from bs4 import BeautifulSoup
import math
from captcha_solver import check_if_captcha


def get_amount_of_pages(url, lst_of_correct_proxies):
    proxy = {'https': random.choice(lst_of_correct_proxies)}
    try:
        resp = requests.get(url, proxies=proxy, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        print(soup.prettify())
        if soup.find('iframe', title='reCAPTCHA'):
            print('reCAPTCHA detected')
            soup = BeautifulSoup(check_if_captcha(url), 'html.parser')
        doctors_amount = int(soup.find('h1',
                                       class_='p-page__title mb-0').get('data-counter').replace("(",
                                                                                                "").replace(")", ""))
        first_page_doctors_amount = len(soup.find_all('span', class_='b-doctor-card__name-surname'))
        if (doctors_amount - first_page_doctors_amount) > 0:
            return math.ceil((doctors_amount - first_page_doctors_amount) / 20) + 1
        else:
            return 1
    except Exception as e:
        print(e)
        get_amount_of_pages(url, lst_of_correct_proxies)


