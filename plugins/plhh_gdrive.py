from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

def plhh_gdrive(gdrv_lk):
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()#executable_path='/usr/local/bin/chromedriver')
    driver.get("https://publiclinks.hashhackers.com/")
    driveid = driver.find_element(By.XPATH, '//*[@id="driveid"]')
    driveid.click()
    driveid.send_keys(gdrv_lk)
    convert = driver.find_element(By.XPATH, '//*[@id="encrypt"]')
    convert.click()
    result = driver.find_element(By.XPATH, '//*[@id="result"]')
    my_link = result.get_attribute('value')
    driver.quit()
    return my_link

