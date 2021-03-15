
from multiprocessing import Queue, cpu_count
from threading import Thread
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time
import sys
import mysql.connector


# Some example data to pass the the selenium processes, this will just cause a sleep of time i
# This data can be a list of any datatype that can be pickled

#selenium_data = [4, 2, 3, 3, 4, 3, 4, 3, 1, 2, 3, 2, 'STOP']

f = open("test.txt")
lines = f.readlines()
f.close()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Milanista.97",
  database="test"
)

mycursor = mydb.cursor()

sql = "INSERT INTO loca_prod (product_name, product_location, qty) VALUES (%s, %s, %s)"
val = []


lines.append('STOP')

selenium_data = lines

# Create the two queues to hold the data and the IDs for the selenium workers
selenium_data_queue = Queue()
worker_queue = Queue()

options = Options()
options.headless = True
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
options.add_experimental_option("prefs", prefs)

#f = open("ProductLocation.txt", "x")
#f = open("ProductLocation.txt", "a")

#f.write("Products around: London" + "\n\n")

# Create Selenium processes and assign them a worker ID
# This ID is what needs to be put on the queue as Selenium workers cannot be pickled
# By default, make one selenium process per cpu core with cpu_count
# TODO: Change the worker creation code to be your webworker of choice e.g. PhantomJS
worker_ids = list(range(cpu_count()))
selenium_workers = {i: webdriver.Chrome(options=options) for i in worker_ids}
for worker_id in worker_ids:
    worker_queue.put(worker_id)

def check_exists_by_css_selector(css_selector, worker):
    try:
        worker.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True

def check_exists_cookie_banner(x_path, worker):
    try:
        worker.find_element_by_xpath(x_path)
    except NoSuchElementException:
        return False
    return True

def selenium_task(worker, data):
    """
    This is a demonstration selenium function that takes a worker and data and then does something with the worker and
    data.
    TODO: change the below code to be whatever it is you want your worker to do e.g. scrape webpages or run browser tests
    :param worker: A selenium web worker NOT a worker ID
    :type worker: webdriver.XXX
    :param data: Any data for your selenium function (must be pickleable)
    :rtype: None
    """
    """
    worker.set_window_size(randint(100, 200), randint(200, 400))
    print("Getting Google")
    worker.get(f'https://google.com')
    print("Sleeping")
    sleep(data)
    """
    counter = 0
    worker.get(data)
    print("\n\n"+data)
    prod_name = data.split("https://www.riverisland.com/p/")[1]
    #f.write(data.split("https://www.riverisland.com/p/")[1] + "\n\n")
    while check_exists_cookie_banner('//*[@id="cookie-notifcation-banner"]/div/button[1]', worker) == True:
        try:
            # Wait for cookie message
            close_icon = WebDriverWait(worker, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="cookie-notifcation-banner"]/div/button[1]')))
            close_icon.click()
            # Wait for cookie message to disappear
            WebDriverWait(worker, 10).until(ec.invisibility_of_element_located((By.XPATH, '//*[@id="cookie-notifcation-banner"]/div/button[1]')))
            print("\nCookie banner closed.\n")
        except:
            print("\nCookie banner not closed. I am trying again.\n")

    

    stateProdSizeBtn = False #not clicked

    while stateProdSizeBtn == False:
        try:
            if check_exists_by_css_selector("#pdp__select-size", worker) == True:
                prod_size_button = WebDriverWait(worker, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#pdp__select-size > li:nth-child("+ str(user_product_size-5) +") > button")))
                if prod_size_button.is_enabled() == True:
                    prod_size_button.click()
                    stateProdSizeBtn = True
                    print("\nProduct size selected.\n")
                else:
                    print("\nProduct size not available for this product.\n")
                    return None
            else:
                prod_size_dropdown = Select(worker.find_element_by_css_selector("#SizeKey"))
                # select by visible text
                try:
                    prod_size_dropdown.select_by_value(str(user_product_size-4))
                    stateProdSizeBtn = True
                    print("\nProduct size selected.\n")
                except NoSuchElementException:
                    print("\nProduct size not available for this product.\n")
                    return None
        except:
            print("Product size not selected. I am trying again.")

    
    #prod_size_dropdown = Select(worker.find_element_by_css_selector("#SizeKey"))
    #try:
        #prod_size_dropdown = select_by_visible_text(str("Size "+user_product_size)+" (UK)")
    #except NoSuchElementException:
        #join()
    
    find_in_store_btn = WebDriverWait(worker, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#pdp-store-stock-checker-link')))
    find_in_store_btn.click() 

    location_inp = WebDriverWait(worker, 20).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/form/div[2]/div/input')))
    location_inp.send_keys(user_location)

    check_availability_btn = WebDriverWait(worker, 20).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="pdp-store-stock-checker-app-container"]/div/aside/div/section/form/button')))
    check_availability_btn.click()

    while True and counter < 2:
        try:
            close_bag = WebDriverWait(worker, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#pdp-store-stock-checker-app-container > div > aside > div > section > section.store-stock-checker__section.store-stock-checker__popup.store-stock-checker__popup--visible > div > button.reset-btn.icon-ui-close.store-stock-checker__popup-close')))
            close_bag.click()
            print("Bag banner closed.")
            break
        except:
            print("Bag banner not closed. I am trying again. Attempt #: ", (counter+1))
            counter = counter + 1

    try:
        location_list = WebDriverWait(worker, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#pdp-store-stock-checker-app-container > div > aside > div > section > section:nth-child(5) > ul')))
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
            val.append(tuple((prod_name, prod_loc, prod_qty)))
            #f.write(prod_loc + "\n" + text_splitted[2] + "\n\n" + "-----------------------" + "\n\n")



def selenium_queue_listener(data_queue, worker_queue):
    """
    Monitor a data queue and assign new pieces of data to any available web workers to action
    :param data_queue: The python FIFO queue containing the data to run on the web worker
    :type data_queue: Queue
    :param worker_queue: The queue that holds the IDs of any idle workers
    :type worker_queue: Queue
    :rtype: None
    """
    print("Selenium func worker started")
    while True:
        current_data = data_queue.get()
        if current_data == 'STOP':
            # If a stop is encountered then kill the current worker and put the stop back onto the queue
            # to poison other workers listening on the queue
            print("STOP encountered, killing worker thread")
            data_queue.put(current_data)
            break
        else:
            print(f"Got the item {current_data} on the data queue")
        # Get the ID of any currently free workers from the worker queue
        worker_id = worker_queue.get()
        worker = selenium_workers[worker_id]
        # Assign current worker and current data to your selenium function
        selenium_task(worker, current_data)
        # Put the worker back into the worker queue as  it has completed it's task
        worker_queue.put(worker_id)
    return


# Create one new queue listener thread per selenium worker and start them
user_location = input("Enter your current location: ")
user_product_size = int(input("Enter your size: "))
start_time = time.time()
print("Starting selenium background processes")
selenium_processes = [Thread(target=selenium_queue_listener,
                             args=(selenium_data_queue, worker_queue)) for _ in worker_ids]
for p in selenium_processes:
    p.daemon = True
    p.start()

# Add each item of data to the data queue, this could be done over time so long as the selenium queue listening
# processes are still running
print("Adding data to data queue")
for d in selenium_data:
    selenium_data_queue.put(d)

# Wait for all selenium queue listening processes to complete, this happens when the queue listener returns
print("Waiting for Queue listener threads to complete")
for p in selenium_processes:
    p.join()

# Quit all the web workers elegantly in the background
print("Tearing down web workers")
for b in selenium_workers.values():
    b.quit()

mycursor.executemany(sql, val)
mydb.commit()

print("Data retrieved.\n\n")
print("Process finished --- %s seconds ---" % round((time.time() - start_time),2))
f.close()