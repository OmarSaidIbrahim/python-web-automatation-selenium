from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://www.riverisland.com/p/black-ri-monogram-panel-runner-trainers-396503')

stateCookieBanner = False #not closed

while stateCookieBanner == False:
    try:
        # Wait for cookie message
        close_icon = WebDriverWait(driver, 5, 0.25).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="cookie-notifcation-banner"]/div/button[1]')))
        close_icon.click()
        # Wait for cookie message to disappear
        WebDriverWait(driver, 5, 0.25).until(ec.invisibility_of_element_located((By.XPATH, '//*[@id="cookie-notifcation-banner"]/div/button[1]')))
        stateCookieBanner = True
    except Exception as e:
        print("\nCookie banner closed\n")

find_in_store_btn = driver.find_element_by_xpath('//*[@id="pdp-store-stock-checker-link"]')
find_in_store_btn.click()

product_size_btn = driver.find_element_by_xpath('//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/form/div[1]/ul/li[1]/button')
product_size_btn.click()

location_inp = driver.find_element_by_xpath('//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/form/div[2]/div/input')
location_inp.send_keys('London')

check_availability_btn = driver.find_element_by_xpath('//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/form/button')
check_availability_btn.click()

close_bag = WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/section[3]/div/button[1]'))).click()

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



