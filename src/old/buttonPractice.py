import time

from selenium import webdriver
from selenium.webdriver import ActionChains


driver = webdriver.Chrome("C:/Users/sambe/chromedriver_win32/chromedriver.exe")
driver.get("https://www.espncricinfo.com/series/sri-lanka-in-england-2021-1239532/england-vs-sri-lanka-2nd-odi-1239535/"
           "ball-by-ball-commentary")

#  dropdown-container comment-inning-dropdown
#input("waiting...")
time.sleep(2)
actionChains = ActionChains(driver)
consent_button = driver.find_element_by_id('onetrust-close-btn-container')
actionChains.move_to_element(consent_button).click().perform()

time.sleep(4)
driver.execute_script("window.scrollTo(0, " + str(500) + ")")
actionChains = ActionChains(driver)
button = driver.find_element_by_class_name('comment-inning-dropdown')
actionChains.move_to_element(button).click().perform()

time.sleep(1)
actionChains = ActionChains(driver)
next_innings_button = driver.find_element_by_class_name('ci-dd__menu')
actionChains.move_to_element_with_offset(next_innings_button, 20, 20).click().perform()

