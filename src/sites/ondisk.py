import re
import os
from selenium import webdriver

chromedriver_path = os.getcwd()
chromedriver_path = re.sub(r"automation_webhard/?.*", "automation_webhard/", chromedriver_path)
chromedriver_path = chromedriver_path + "chromedriver"
driver = webdriver.Chrome(chromedriver_path)

if __name__ == '__main__':
    print()
