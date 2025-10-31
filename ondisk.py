import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import time # 디버깅 및 alert 대기를 위해 time 임포트

# .env 파일에서 환경 변수(ID, PW) 불러오기
load_dotenv()

# [참고 코드 반영] User-Agent는 stealth가 설정하도록 비워둡니다.

class Ondisk:
    def __init__(self):
        # .env 파일에서 계정 정보 불러오기
        self.user_id = os.environ.get("ONDISK_ID")
        self.user_pass = os.environ.get("ONDISK_PW")

        if not self.user_id or not self.user_pass:
            print("오류: ONDISK_ID 또는 ONDISK_PW 환경 변수가 설정되지 않았습니다.")
            print(".env 파일을 확인해주세요.")
            sys.exit(1) # 스크립트 중지
        
        # [로직 변경] 메인 페이지는 더 이상 사용하지 않습니다.
        self.event_page = "https://www.ondisk.co.kr/index.php?mode=eventMarge&sm=event&action=view&idx=746&event_page=1"
        self.browser = None

    def _init_driver(self):
        """
        웹 드라이버를 초기화하고 봇 감지 우회 옵션을 설정
        """
        chrome_options = webdriver.ChromeOptions()
        
        chrome_options.add_argument('incognito') # 시크릿 모드
        chrome_options.add_argument("disable-extensions") # 확장 프로그램 비활성화
        chrome_options.add_argument('--log-level=3') # 로그 레벨 낮춤
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)


# --- ⬇️ GitHub Actions를 위한 코드 ⬇️ ---
        # 'CI' 환경 변수가 'true'이거나 존재할 경우 (GitHub Actions의 기본값)
        if os.environ.get('CI'):
            print("CI 환경 감지. Headless 모드로 실행합니다.")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox") # CI 환경에서 필수
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")

        service = Service(executable_path=ChromeDriverManager().install()) 
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Stealth 모드 적용
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        return driver

    def wait_for_xpath_element(self, xpath, timeout=15):
        """
        지정한 XPath를 가진 요소를 기다림 (기본 15초)
        """
        try:
            element = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except TimeoutException:
            # print(f"페이지 로딩 실패 (Timeout). xpath: {xpath}") # 이 부분은 예외처리로 넘김
            raise # TimeoutException을 그대로 발생시킴
        except NoSuchElementException:
            # print(f"요소를 찾을 수 없음 (NoSuchElement). xpath: {xpath}")
            raise # NoSuchElementException을 그대로 발생시킴

    def wait_for_alert(self, timeout=3):
        """
        알림(Alert) 창을 기다리고 확인 버튼을 누름
        """
        try:
            WebDriverWait(self.browser, timeout).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"알림 발견: {alert_text}")
            alert.accept()
            return alert_text
        except TimeoutException:
            # 알림 창이 뜨지 않으면 그냥 통과
            return None

    def run(self):
        try:
            self.browser = self._init_driver()
            print("브라우저 시작. 이벤트 페이지로 직접 이동합니다.")
            
            # [로직 변경] 메인 페이지 대신 이벤트 페이지로 바로 이동
            self.browser.get(self.event_page)

            # --- 로그인 시도 ---
            try:
                # [참고 코드 반영] 10초 내로 로그인 폼(name='mb_id')이 보이는지 확인
                # XPATH를 사용하여 name 속성으로 요소를 찾음
                id_element = self.wait_for_xpath_element("//input[@name='mb_id']", timeout=10)
                
                # 로그인 폼이 나타났으므로 로그인을 수행
                print("로그인 폼 발견. 로그인을 시도합니다.")
                password_element = self.browser.find_element(By.NAME, "mb_pw")
                
                id_element.send_keys(self.user_id)
                password_element.send_keys(self.user_pass)

                # [참고 코드 반영] 로그인 버튼 XPATH 사용
                login_button = self.browser.find_element(By.XPATH, "//*[@id='page-login']/form/fieldset/div/p[3]")
                login_button.click()
                print("로그인 버튼 클릭.")

                # 로그인 직후 팝업 알림 처리
                self.wait_for_alert(timeout=3)
                print("로그인 성공. 룰렛 페이지 로딩을 대기합니다.")
                
                # 페이지가 리로드될 수 있으므로 잠시 대기
                time.sleep(2) 

            except (TimeoutException, NoSuchElementException):
                # 10초 내로 로그인 폼이 안 보이면, 이미 로그인된 것으로 간주
                print("로그인 폼이 없음. 이미 로그인된 상태로 간주합니다.")

            self.browser.get(self.event_page)
            self.wait_for_alert(timeout=5)
            time.sleep(5)
            
            # --- 룰렛 클릭 (로그인 직후 or 이미 로그인된 상태) ---
            print("룰렛 iframe을 찾습니다...")
            
            # [원본 코드 로직] iframe으로 전환
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
            # # [디버깅] 오류 발생 시 스크린샷 및 HTML 저장
            # try:
            #     if self.browser:
            #         self.browser.save_screenshot("error_screenshot.png")
            #         print("에러 스크린샷을 'error_screenshot.png'로 저장했습니다.")
                    
            #         # 렌더링된 HTML 저장
            #         rendered_html = self.browser.find_element(By.TAG_NAME, 'html').get_attribute('outerHTML')
            #         with open("error_page_source.html", "w", encoding="utf-8") as f:
            #             f.write(rendered_html)
            #         print("현재 페이지 소스를 'error_page_source.html' 파일로 저장했습니다.")
            # except:
            #     print("디버그 파일 저장 실패.")
        
        finally:
            # 스크립트가 성공하든 실패하든 항상 브라우저를 종료
            if self.browser:
                self.browser.quit()
                print("브라우저를 종료했습니다.")


if __name__ == '__main__':
    ondisk = Ondisk()
    ondisk.run()