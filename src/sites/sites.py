"""
trouble shooting
site라고 지으면 pycharm debugger가 socket closed 라고 하면서 실행 불가능 상태로 변경된다.
https://superuser.com/questions/1385995/my-pycharm-run-is-working-but-debugging-is-failing

"""
import os
import re
import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logger import logger
from utils.account import ACCOUNT_FILE_PATH, DEFAULT_ACCOUNT_VALUE

IE_AGENT = "Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"

chromedriver_path = os.getcwd()
chromedriver_path = re.sub(r"automation_webhard/?.*", "automation_webhard/", chromedriver_path)
chromedriver_path = chromedriver_path + "chromedriver"


def init_chrome_driver(options=None):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(options)
    driver = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)
    return driver


class Site:
    def __init__(self, site_name, options=None):
        self.site_name = site_name
        self.options = options
        self.browser = None

        self.account = self.load_account_info()

    def load_account_info(self):
        with open(ACCOUNT_FILE_PATH, "r") as f:
            account_info = json.load(f)
            account_id = account_info[self.site_name]['id']
            account_pw = account_info[self.site_name]['pw']

            if account_id == DEFAULT_ACCOUNT_VALUE or account_pw == DEFAULT_ACCOUNT_VALUE:
                logger.error(f"{self.site_name}의 ID 혹은 PW의 갱신이 필요합니다.")
                raise
        return {"id": account_id, "pw": account_pw}

    def wait_for_xpath_element_located(self, xpath, time=3):
        """
        페이지 로딩이 끝난 후 해당 element가 존재 하는지 확인하는 기능
        :param xpath:
        :param time:
        :return:
        """
        try:
            element = WebDriverWait(self.browser, time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except TimeoutException:

            logger.error(f"페이지 로딩을 실패했습니다. xpath: {xpath}")
            raise
        except NoSuchElementException:
            logger.error(f"해당 element가 존재하지않습니다. xpath: {xpath}")
            raise

    def wait_for_alert_present(self, time=3):
        """
        페이지 로딩이 끝난 후 해당 element가 존재 하는지 확인하는 기능
        :param error_message:
        :param time:
        :return:
        """
        try:
            WebDriverWait(self.browser, time).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            alert.accept()
        except TimeoutException:
            pass

    def run(self):
        pass
