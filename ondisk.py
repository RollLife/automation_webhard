import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# .env 파일에서 환경 변수(ID, PW) 불러오기
load_dotenv()

IE_AGENT = "Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"

class Ondisk:
    def __init__(self):
        # .env 파일에서 계정 정보 불러오기
        self.user_id = os.environ.get("ONDISK_ID")
        self.user_pass = os.environ.get("ONDISK_PW")

        if not self.user_id or not self.user_pass:
            print("오류: ONDISK_ID 또는 ONDISK_PW 환경 변수가 설정되지 않았습니다.")
            print(".env 파일을 확인해주세요.")
            sys.exit(1) # 스크립트 중지

        self.user_agent = IE_AGENT
        self.main_page = "https://www.ondisk.co.kr/index.php"
        self.event_page = "https://ondisk.co.kr/index.php?mode=eventMarge&sm=event&action=view&idx=746&event_page=1"
        self.browser = None

    def _init_driver(self):
        """
        웹 드라이버를 초기화하고 GitHub Actions 환경에 최적화된 옵션을 설정
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--user-agent="{self.user_agent}"')
        
        # --- GitHub Actions 또는 Linux 서버 환경을 위한 옵션 ---
        # chrome_options.add_argument("--headless") # GUI 없이 백그라운드에서 실행
        # chrome_options.add_argument("--no-sandbox") # Docker/CI 환경에서 필요
        # chrome_options.add_argument("--disable-dev-shm-usage") # 공유 메모리 문제 방지
        # chrome_options.add_argument("--disable-gpu") # GPU 가속 비활성화
        # chrome_options.add_argument("--window-size=1920x1080") # 적절한 해상도 설정
        # -----------------------------------------------------

        # Selenium 4부터는 Service() 객체를 사용하는 것이 표준
        # chromedriver를 자동으로 다운로드하고 관리해줌
        service = Service(executable_path=ChromeDriverManager().install()) 
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def wait_for_xpath_element(self, xpath, timeout=5):
        """
        지정한 XPath를 가진 요소를 기다림 (기본 5초)
        """
        try:
            element = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except TimeoutException:
            print(f"페이지 로딩 실패 (Timeout). xpath: {xpath}")
            raise
        except NoSuchElementException:
            print(f"요소를 찾을 수 없음 (NoSuchElement). xpath: {xpath}")
            raise

    def wait_for_alert(self, timeout=3):
        """
        알림(Alert) 창을 기다리고 확인 버튼을 누름
        """
        try:
            WebDriverWait(self.browser, timeout).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            alert.accept()
            return alert_text
        except TimeoutException:
            # 알림 창이 뜨지 않으면 그냥 통과
            return None

    def run(self):
        try:
            self.browser = self._init_driver()
            print("브라우저 시작. 메인 페이지로 이동합니다.")
            self.browser.get(self.main_page)

            # 로그인
            id_element = self.wait_for_xpath_element(".//div[@class='insert']/p[1]/input")
            password_element = self.wait_for_xpath_element(".//div[@class='insert']/p[2]/input")

            id_element.send_keys(self.user_id)
            password_element.send_keys(self.user_pass)

            # Selenium 4 문법으로 변경
            login_button = self.browser.find_element(By.XPATH, ".//p[@class='btn-login']")
            login_button.click()
            print("로그인 시도...")

            # 로그인 직후 이벤트 알림 처리
            self.wait_for_alert(timeout=2)
            print("로그인 성공. 출석체크 페이지로 이동합니다.")

            # 출석체크 페이지 이동
            self.browser.get(self.event_page)

            # iframe으로 전환
            iframe = self.wait_for_xpath_element(".//div[@id='page-contents']//iframe", timeout=10)
            self.browser.switch_to.frame(iframe)
            print("이벤트 페이지 iframe으로 전환 완료.")

            # 룰렛 버튼 클릭
            roulette_button = self.wait_for_xpath_element(".//div[@id='js-roulette']/p/button")
            roulette_button.click()
            print("룰렛 버튼 클릭.")

            # 결과 알림 처리
            alert_text = self.wait_for_alert(timeout=10) # 룰렛 도는 시간 대기

            if alert_text:
                if "오늘 이미 출석하셨습니다" in alert_text:
                    print("결과: 오늘은 이미 출석한 상태입니다.")
                else:
                    print(f"결과: {alert_text}")
            else:
                print("룰렛 실행 후 알림 창을 감지하지 못했습니다 (Timeout).")

            print("스크립트 실행 완료.")

        except Exception as e:
            print(f"스크립트 실행 중 예외 발생: {e}")
        
        finally:
            # 스크립트가 성공하든 실패하든 항상 브라우저를 종료
            if self.browser:
                self.browser.quit()
                print("브라우저를 종료했습니다.")


if __name__ == '__main__':
    ondisk = Ondisk()
    ondisk.run()
    
    # https://jakpentest.tistory.com/entry/Github-Action%EC%97%90%EC%84%9C-Selenium-%EC%8B%A4%ED%96%89%EC%8B%9C%ED%82%A4%EA%B8%B0