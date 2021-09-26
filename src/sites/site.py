import os
import re
import json

from selenium import webdriver

from utils.account import ACCOUNT_FILE_PATH, DEFAULT_ACCOUNT_VALUE

IE_AGENT = "Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"

chromedriver_path = os.getcwd()
chromedriver_path = re.sub(r"automation_webhard/?.*", "automation_webhard/", chromedriver_path)
chromedriver_path = chromedriver_path + "chromedriver"


class Site:
    def __init__(self, site_name):
        self.site_name = site_name
        self.account = self.load_account_info()

    def load_account_info(self):
        with open(ACCOUNT_FILE_PATH, "r") as f:
            account_info = json.load(f)
            account_id = account_info[self.site_name]['id']
            account_pw = account_info[self.site_name]['pw']

            if account_id == DEFAULT_ACCOUNT_VALUE or account_pw == DEFAULT_ACCOUNT_VALUE:
                # TODO: must need to change logging module
                raise
        return {"id": account_id, "pw": account_pw}

    def init_chrome_driver(self, chrome_driver_path, chrome_options=None):
        if chrome_options:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument(chrome_options)
        driver = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)
        return driver

    def run(self):
        pass
