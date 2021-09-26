import re
import os
import json
import time
from selenium import webdriver

account_file_path = os.getcwd()
account_file_path = re.sub(r"automation_webhard/?.*", "automation_webhard/auth/account.json", account_file_path)

default_account_value = "$set_plz"

if not os.path.exists(account_file_path):
    default_ondisk_account = {"ondisk": {"id": default_account_value, "pw": default_account_value}}

    f = open(account_file_path, "w")
    json.dump(default_ondisk_account, f)
    f.close()

with open(account_file_path, "r") as f:
    account_info = json.load(f)
    ondisk_id = account_info['ondisk']['id']
    ondisk_pw = account_info['ondisk']['pw']

    if ondisk_id == default_account_value or ondisk_pw == default_account_value:
        print("plz reset ondisk_account")

chromedriver_path = os.getcwd()
chromedriver_path = re.sub(r"automation_webhard/?.*", "automation_webhard/", chromedriver_path)
chromedriver_path = chromedriver_path + "chromedriver"
driver = webdriver.Chrome(chromedriver_path)

driver.get("http://www.ondisk.co.kr/index.php")

time.sleep(1)

print(driver.page_source)
id_element = driver.find_element_by_xpath(".//div[@class='insert']/p[1]/input")
id_element.send_keys(ondisk_id)
password_element = driver.find_element_by_xpath(".//div[@class='insert']/p[2]/input")
password_element.send_keys(ondisk_pw)

if __name__ == '__main__':
    print()
