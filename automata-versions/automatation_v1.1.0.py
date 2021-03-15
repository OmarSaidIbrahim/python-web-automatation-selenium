from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time
import mysql.connector
import sys

def check_exists_by_css_selector(css_selector):
    try:
        driver.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True

start_time = time.time()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Milanista.97",
  database="test"
)

mycursor = mydb.cursor()

#f = open("MenShoesLinks_v1.0.1.txt")
f = open("test.txt")
lines = f.readlines()
f.close()

options = Options()
options.headless = True
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(options=options)

stateCookieBanner = False #not closed
counter = 0

f = open("ProductLocation.txt", "x")
f = open("ProductLocation.txt", "a")

f.write("Products around: London" + "\n\n")

for line in lines:
    print("\n\n"+line)
    driver.get(line)
    prod_name = line.split("https://www.riverisland.com/p/")[1]
    f.write(line.split("https://www.riverisland.com/p/")[1] + "\n\n")
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
            if check_exists_by_css_selector("#pdp-store-stock-checker-app-container > div > aside > div > section > form > div.size-selector > ul > li:nth-child(2) > button") == True:
                product_size_btn = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#pdp-store-stock-checker-app-container > div > aside > div > section > form > div.size-selector > ul > li:nth-child(2) > button')))
                product_size_btn.click()
                stateProdSizeBtn = True
                print("\nProduct size selected.\n")
            else:
                select = Select(driver.find_element_by_css_selector('#pdp-store-stock-checker-app-container > div > aside > div > section > form > div.size-selector > div > select'))
                # select by visible text
                select.select_by_visible_text('7 (UK)')
                stateProdSizeBtn = True
                print("\nProduct size selected.\n")
        except:
            print("Product size not selected. I am trying again.")

    location_inp = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/form/div[2]/div/input')))
    location_inp.send_keys('London')

    check_availability_btn = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/form/button')))
    check_availability_btn.click()

    while True or counter < 3:
        try:
            close_bag = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#pdp-store-stock-checker-app-container > div > aside > div > section > section.store-stock-checker__section.store-stock-checker__popup.store-stock-checker__popup--visible > div > button.reset-btn.icon-ui-close.store-stock-checker__popup-close')))
            close_bag.click()
            print("Bag banner closed.")
            break
        except:
            print("Bag banner not closed. I am trying again. Attempt #: " + (counter+1))
            counter = counter + 1
    
    while True:
        try:
            WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, '#pdp-store-stock-checker-app-container > div > aside > div > section > section:nth-child(5) > button'))).click()
            time.sleep(0.5) #a loader pops up and the automata cannot click because the button is invisible
        except Exception as e:
            print("\nPoduct locations loaded\n")
            break

    try:
        location_list = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#pdp-store-stock-checker-app-container > div > aside > div > section > section:nth-child(5) > ul')))
        locations = location_list.find_elements_by_tag_name('li')
    except TimeoutException as ex:
        print(ex)
        sys.exit()
    

            
    for location in locations:
        text = location.text
        text_splitted = text.split("\n")
        prod_loc = text_splitted[0]
        #prod_qty = text_splitted[2]
        if text_splitted[2] == "Out of stock":
            prod_qty = 0
        else:
            prod_qty = 1
            sql = "INSERT INTO loca_prod (product_name, product_location, qty) VALUES (%s, %s, %s)"
            val = (prod_name, prod_loc, prod_qty)
            mycursor.execute(sql, val)
            f.write(prod_loc + "\n" + text_splitted[2] + "\n\n" + "-----------------------" + "\n\n")
        
#mydb.commit()

print(mycursor.rowcount, "record inserted.")

print("Data retrieved.\n\n")
print("Process finished --- %s seconds ---" % round((time.time() - start_time),2))
f.close()
driver.quit()