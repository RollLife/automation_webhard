import re
import os
import json
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium import webdriver

site_name = "ondisk"

account_file_path = os.getcwd()
account_file_path = re.sub(r"automation_webhard/?.*", "automation_webhard/auth/account.json", account_file_path)

default_account_value = "$set_plz"

if not os.path.exists(account_file_path):
    default_ondisk_account = {site_name: {"id": default_account_value, "pw": default_account_value}}

    f = open(account_file_path, "w")
    json.dump(default_ondisk_account, f)
    f.close()

with open(account_file_path, "r") as f:
    account_info = json.load(f)
    ondisk_id = account_info[site_name]['id']
    ondisk_pw = account_info[site_name]['pw']

    if ondisk_id == default_account_value or ondisk_pw == default_account_value:
        print(f"plz reset {site_name} account info")

chromedriver_path = os.getcwd()
chromedriver_path = re.sub(r"automation_webhard/?.*", "automation_webhard/", chromedriver_path)
chromedriver_path = chromedriver_path + "chromedriver"

print(ondisk_id, ondisk_pw)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--user-agent="Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"')
driver = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)

driver.get("http://www.ondisk.co.kr/index.php")

time.sleep(1)

# print(driver.page_source)
id_element = driver.find_element_by_xpath(".//div[@class='insert']/p[1]/input")
id_element.send_keys(ondisk_id)
password_element = driver.find_element_by_xpath(".//div[@class='insert']/p[2]/input")
password_element.send_keys(ondisk_pw)

login_button = driver.find_element_by_xpath(".//p[@class='btn-login']")
login_button.click()

# 이벤트 기간중 alert 된 메시지가 발생했을 경우
try:
    WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')

    alert = driver.switch_to.alert
    alert.accept()
    print("alert accepted")
except TimeoutException:
    print("no alert")

driver.get("http://www.ondisk.co.kr/index.php")

# 결제 이벤트 팝업 해당 팝업을 닫아야 버튼이 눌림(페이지 전체 영역에 팝업이 발생)
event_popup_close = driver.find_element_by_xpath(".//div[@id='js-charge-layer']/p[@class='btn_close']")
event_popup_close.click()

time.sleep(1)

# 출석체크
# check_button = driver.find_element_by_xpath(".//ul[@class='etc_button']/li[@class='check']")
# check_button.click()
#
# time.sleep(1)

# 출석체크 페이지를 클릭하여 이동이 되지 않아 강제 페이지 이동
driver.get(
    "https://ondisk.co.kr/event/20140409_attend/event.php?mode=eventMarge&sm=event&action=view&idx=746&event_page=1")

print(driver.page_source)
roulette_button = driver.find_element_by_xpath(".//div[@id='js-roulette']/p/button")
roulette_button.click()

try:
    WebDriverWait(driver, 5).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')

    alert = driver.switch_to.alert
    alert.accept()
    print("alert accepted")
except TimeoutException:
    print("no alert")


# TODO: alert 내용 확인하여 '오늘 이미 출석하셨습니다' 해당 내용이 나오면 완료 혹은 넘어가도록 하기
# TODO: 테스트 구현 및 구조화 완료
# TODO: 윈도우 환경에서 구동 확인
# TODO: 모니터링 도구 및 백그라운드 실행 혹은 자동 실행 도구 필요

driver.close()

if __name__ == '__main__':
    print()
