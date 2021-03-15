from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

start_time = time.time()

options = Options()
options.headless = True
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.get('https://www.riverisland.com/c/men/shoes-and-boots')

stateCookieBanner = False #not closed

while stateCookieBanner == False:
    try:
        # Wait for cookie message
        close_icon = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#cookie-notifcation-banner > div > button.cookie-notification-banner__button-remove.icon-ui-close')))
        close_icon.click()
        # Wait for cookie message to disappear
        WebDriverWait(driver, 20).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, '#cookie-notifcation-banner > div > button.cookie-notification-banner__button-remove.icon-ui-close')))
        stateCookieBanner = True
        print("\nCookie banner closed\n")
    except Exception as e:
        print("\nCookie banner not closed. I am trying again.\n")

#load all the products by clicking the button "load more" until it disappear
while True:
    try:
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, '#__next > div > div.LoadingFetchMoreWrapper__loading-fetch-more-wrapper___2ieY8 > div > a > button'))).click()
    except:
        print("Poduct page loaded\n")
        break

f = open("MenShoesLinks_API.txt", "w")

#for each element "a", of the section that contains 
#all the product, write the urls (href) on the txt file

elements = driver.find_elements_by_css_selector("#__next > div > div.Grid__container___nxt1I > div.MainLoader__productListing___1ZaKr > section > a")
for el in elements:
    f.write(el.get_attribute("href")[-6:] + "\n")

f.close()
driver.quit()
print("Writing Complete\n")
print("Process finished --- %s seconds ---" % round((time.time() - start_time),2))