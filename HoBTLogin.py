from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
import os

# Check if chrome driver is installed or not
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver.exe'
if os.path.exists(driver_path):
    print(f"chrom driver is insatlled: {driver_path}")
else:
    print(f"install the chrome driver(ver: {chrome_ver})")
    chromedriver_autoinstaller.install(True)

# Get driver and open url
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

driver.get("http://3.37.135.228/")
time.sleep(3)

driver.find_element(By.XPATH, '//*[@id="navbarSupportedContent"]/ul/li[1]/a').click()
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys("admin")
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("qwer1234")
driver.find_element(By.XPATH, '/html/body/div/form/button').click()
time.sleep(100)