import re
import os
import json
import time
from selenium import webdriver

chromedriver_path = os.getcwd()
chromedriver_path = re.sub(r"automation_webhard/?.*", "automation_webhard/", chromedriver_path)
chromedriver_path = chromedriver_path + "chromedriver"
driver = webdriver.Chrome(chromedriver_path)

driver.get("http://www.ondisk.co.kr/index.html")

time.sleep(1)
id_element = driver.find_element_by_xpath(".//div[@class='page-login']/form/fieldset/div[@class='insert']/p[1]/input")
password_element = driver.find_element_by_xpath(".//div[@class='page-login']/form/fieldset/div[@class='insert']/p[2]/input")

driver.f


if __name__ == '__main__':
    print()
