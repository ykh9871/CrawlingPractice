from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.opinet.co.kr/user/main/mainView.do")
time.sleep(1)
driver.get("https://www.opinet.co.kr/searRgSelect.do")
time.sleep(1)

driver.find_element(By.XPATH, '//*[@id="SIDO_NM0"]/option[2]').click()
time.sleep(2)
seoul_list = driver.find_element(By.ID, 'SIGUNGU_NM0')
seoul_gu_list = seoul_list.find_elements(By.TAG_NAME, "option")

seoul_gu_name = [option.get_attribute("value") for option in seoul_gu_list]
seoul_gu_name.remove('')
print(seoul_gu_name)

for i in seoul_gu_name:
    driver.find_element(By.ID, 'SIGUNGU_NM0').send_keys(i)

    # 조회 버튼 누르기
    driver.find_element(By.ID, 'searRgSelect').click()
    time.sleep(2)

    # 엑셀 저장 버튼 누르기
    driver.find_element(By.XPATH, '//*[@id="glopopd_excel"]/span').click()
    time.sleep(2)