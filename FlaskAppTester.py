from selenium import webdriver
import time
driver = webdriver.Chrome()
driver.implicitly_wait(0.5)
driver.maximize_window()

driver.get("http://127.0.0.1:5000/")
time.sleep(10)
#to identify element
s = driver.find_element_by_xpath("//input[@type='file']")
#file path specified with send_keys
s.send_keys("umsatz.csv")