import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium import webdriver

from src.sites.sites import Site, IE_AGENT, chromedriver_path


# TODO: alert 내용 확인하여 '오늘 이미 출석하셨습니다' 해당 내용이 나오면 완료 혹은 넘어가도록 하기
# TODO: 테스트 구현 및 구조화 완료
# TODO: 윈도우 환경에서 구동 확인
# TODO: 모니터링 도구 및 백그라운드 실행 혹은 자동 실행 도구 필요
# TODO: 로깅 모듈 추가
# TODO: pylint 추가
# TODO: issue 모두 정리


class Ondisk(Site):
    def __init__(self):
        site_name = "ondisk"
        option = f'--user-agent="{IE_AGENT}"'
        self.main_page = "https://www.ondisk.co.kr/index.php"

        super().__init__(site_name, option)

    def run(self):
        self.browser.get(self.main_page)

        # TODO: 페이지 로딩을 위해 정해진 시간으로 기다리는 해당 방법은 수정해야만 한다.
        id_element = self.wait_for_xpath_element_located(".//div[@class='insert']/p[1]/input")
        password_element = self.wait_for_xpath_element_located(".//div[@class='insert']/p[2]/input")

        id_element.send_keys(self.account['id'])
        password_element.send_keys(self.account['pw'])

        login_button = self.browser.find_element_by_xpath(".//p[@class='btn-login']")
        login_button.click()

        # 이벤트 기간중 alert 된 메시지가 발생했을 경우
        self.wait_for_alert_present(time=2)

        self.browser.get(self.main_page)

        # 결제 이벤트 팝업 해당 팝업을 닫아야 버튼이 눌림(페이지 전체 영역에 팝업이 발생)
        try:
            event_popup_close = WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((By.XPATH, ".//div[@id='js-charge-layer']/p[@class='btn_close']"))
            )
            event_popup_close.click()
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        # 출석체크
        # check_button = browser.find_element_by_xpath(".//ul[@class='etc_button']/li[@class='check']")
        # check_button.click()
        #
        # time.sleep(1)

        # 출석체크 페이지를 클릭하여 이동이 되지 않아 강제 페이지 이동
        self.browser.get(
            "https://ondisk.co.kr/event/20140409_attend/event.php?mode=eventMarge&sm=event&action=view&idx=746&event_page=1")

        roulette_button = self.wait_for_xpath_element_located(".//div[@id='js-roulette']/p/button")
        roulette_button.click()

        # TODO: 룰렛 작동시간 파악
        try:
            WebDriverWait(self.browser, 10).until(EC.alert_is_present())

            alert = self.browser.switch_to.alert
            if "오늘 이미 출석하셨습니다" in alert.text:
                print("오늘은 이미 출석한 상태")
            else:
                print(alert.text)
            alert.accept()
            # TODO: 이때 어떤 알림인지 알 수 있어야한다.
            # 정상적으로 출석이 되었는지 아니면 출석이 이미 되었는지 판단의 재료가 되기 대문

        except TimeoutException:
            print("no alert")

        self.browser.quit()


if __name__ == '__main__':
    ondisk = Ondisk()
    ondisk.run()
