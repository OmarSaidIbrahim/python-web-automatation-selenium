from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

start_time = time.time()

#f = open("MenShoesLinks_v1.0.1.txt")
f = open("test.txt")
lines = f.readlines()
f.close()

options = Options()
options.headless = True
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
options.add_experimental_option("prefs", prefs)

#options=options

driver = webdriver.Chrome(options=options)

stateCookieBanner = False #not closed
stateCloseBag = False #not closed

f = open("ProductLocation.txt", "x")
f = open("ProductLocation.txt", "a")

f.write("Products around: London" + "\n\n")

for line in lines:
    print("\n\n"+line)
    driver.get(line)
    f.write("*"+line.split("https://www.riverisland.com/p/")[1]+"*" + "\n\n")
    while stateCookieBanner == False:
        try:
            # Wait for cookie message
            close_icon = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="cookie-notifcation-banner"]/div/button[1]')))
            close_icon.click()
            # Wait for cookie message to disappear
            WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.XPATH, '//*[@id="cookie-notifcation-banner"]/div/button[1]')))
            stateCookieBanner = True
            print("\nCookie banner closed.\n")
        except:
            print("\nCookie banner not closed. I am trying again.\n")

    find_in_store_btn = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="pdp-store-stock-checker-link"]')))
    find_in_store_btn.click() 

    stateProdSizeBtn = False #not clicked

    while stateProdSizeBtn == False:
        try:
            product_size_btn = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#pdp-store-stock-checker-app-container > div > aside > div > section > form > div.size-selector > ul > li:nth-child(1) > button')))
            product_size_btn.click()
            stateProdSizeBtn = True
            print("\nProduct size selected.\n")
        except:
            print("Product size not selected. I am trying again.")

    location_inp = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/form/div[2]/div/input')))
    location_inp.send_keys('London')

    check_availability_btn = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/form/button')))
    check_availability_btn.click()

    while stateCloseBag == False:
        try:
            close_bag = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#pdp-store-stock-checker-app-container > div > aside > div > section > section.store-stock-checker__section.store-stock-checker__popup.store-stock-checker__popup--visible > div > button.reset-btn.icon-ui-close.store-stock-checker__popup-close')))
            close_bag.click()
            stateCloseBag = True
            print("Bag banner closed.")
        except:
            print("Bag banner not closed. I am trying again.")
    
    """while True:
        try:
            WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/section[2]/button'))).click()
            time.sleep(0.5) #a loader pops up and the automata cannot click because the button is invisible
        except Exception as e:
            print("\nPoduct locations loaded\n")
            break"""

    location_list = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#pdp-store-stock-checker-app-container > div > aside > div > section > section:nth-child(5) > ul')))
    locations = location_list.find_elements_by_tag_name('li')
            
    for location in locations:
        text = location.text
        f.write(text + "\n\n" + "-----------------------" + "\n\n")

print("Data retrieved.\n\n")
print("Process finished --- %s seconds ---" % round((time.time() - start_time),2))
f.close()
driver.quit()