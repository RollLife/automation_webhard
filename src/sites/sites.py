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

from utils.account import ACCOUNT_FILE_PATH, DEFAULT_ACCOUNT_VALUE

IE_AGENT = "Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"

chromedriver_path = os.getcwd()
chromedriver_path = re.sub(r"automation_webhard/?.*", "automation_webhard/", chromedriver_path)
chromedriver_path = chromedriver_path + "chromedriver"


class Site:
    def __init__(self, site_name, options=None):
        self.site_name = site_name
        self.account = self.load_account_info()
        self.browser = self.init_chrome_driver(options=options)

    def load_account_info(self):
        with open(ACCOUNT_FILE_PATH, "r") as f:
            account_info = json.load(f)
            account_id = account_info[self.site_name]['id']
            account_pw = account_info[self.site_name]['pw']

            if account_id == DEFAULT_ACCOUNT_VALUE or account_pw == DEFAULT_ACCOUNT_VALUE:
                # TODO: must need to change logging module
                raise
        return {"id": account_id, "pw": account_pw}

    def init_chrome_driver(self, options=None):
        if options:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument(options)
            driver = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)
        else:
            driver = webdriver.Chrome(chromedriver_path)
        return driver

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

            # TODO: 로깅 모듈을 추가하고 제대로된 문구를 추가할 수 있도록 한다.
            print(f"페이지 로딩을 실패했습니다. xpath: {xpath}")
            raise
        except NoSuchElementException:
            # TODO: 로깅 모듈을 추가하고 제대로된 문구를 추가할 수 있도록 한다.
            print(f"해당 element가 존재하지않습니다. xpath: {xpath}")
            raise

    def wait_for_alert_present(self, time=3, error_message="해당 알림이 확인 되지 않았습니다."):
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
            # TODO: 로깅 모듈을 추가하고 제대로된 문구를 추가할 수 있도록 한다.
            print(error_message)

    def run(self):
        pass
