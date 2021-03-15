from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://www.riverisland.com/c/men/shoes-and-boots')

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
        print(e)

print("\nCookie banner closed\n")

#load all the products by clicking the button "load more" until it disappear
while True:
    try:
        load_more = WebDriverWait(driver, 5, 0.25).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#__next > div > div.LoadingFetchMoreWrapper__loading-fetch-more-wrapper___2ieY8 > div > a > button')))
        load_more.click()
    except Exception as e:
        print("Poduct page loaded\n")
        break

print("Loading Complete")

f = open("MenShoesLinks_v1.0.0.txt", "x")
f = open("MenShoesLinks_v1.0.0.txt", "a")

#for each element "a", of the section that contains 
#all the product, write the urls (href) on the txt file
elements = driver.find_elements_by_css_selector("#__next > div > div.Grid__container___nxt1I > div.MainLoader__productListing___1ZaKr > section > a")
for el in elements:
    f.write(el.get_attribute("href") + "\n")

f.close()
print("Writing Complete")
driver.quit()