from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_recaptcha_solver import RecaptchaSolver
import time



def check_if_captcha(url):
    """Check if url is available and if not - solving captcha"""
    test_ua = ('Mozilla/5.0 (Windows NT 4.0; WOW64) '
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36')
    options = Options()
    options.add_argument(f'--user-agent={test_ua}')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument("--headless")
    test_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    solver = RecaptchaSolver(driver=test_driver)
    test_driver.get(url)
    try:
        recaptcha_iframe = test_driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        time.sleep(2)
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        time.sleep(2)
        return test_driver.page_source
    except:
        return test_driver.page_source