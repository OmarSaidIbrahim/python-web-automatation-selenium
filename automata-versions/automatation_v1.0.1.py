from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

f = open("WomenShoesLinks_v1.0.1.txt")
line = f.readline()
f.close()

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)
driver.get(line)

stateCookieBanner = False #not closed

while stateCookieBanner == False:
    try:
        # Wait for cookie message
        close_icon = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="cookie-notifcation-banner"]/div/button[1]')))
        close_icon.click()
        # Wait for cookie message to disappear
        WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.XPATH, '//*[@id="cookie-notifcation-banner"]/div/button[1]')))
        stateCookieBanner = True
        print("\nCookie banner closed\n")
    except Exception as e:
        print("\nCookie banner closed\n")

find_in_store_btn = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="pdp-store-stock-checker-link"]')))
find_in_store_btn.click()

product_size_btn = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#pdp-store-stock-checker-app-container > div > aside > div > section > form > div.size-selector > ul > li:nth-child(1) > button')))
product_size_btn.click()

location_inp = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/form/div[2]/div/input')))
location_inp.send_keys('London')

check_availability_btn = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/form/button')))
check_availability_btn.click()

close_bag = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#pdp-store-stock-checker-app-container > div > aside > div > section > section.store-stock-checker__section.store-stock-checker__popup.store-stock-checker__popup--visible > div > button.reset-btn.icon-ui-close.store-stock-checker__popup-close')))
close_bag.click()

location_list = driver.find_element_by_xpath('//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/section[2]/ul')
locations = location_list.find_elements_by_tag_name('li')
for location in locations:
    text = location.text
    print(text)

f = open("ProductLocation.txt", "x")
f = open("ProductLocation.txt", "a")
for location in locations:
    text = location.text
    f.write(text + "\n\n")
    
f.close()

driver.quit()



