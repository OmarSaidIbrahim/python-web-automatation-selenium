import requests
import json
from geopy.geocoders import Nominatim
from scraper_api import ScraperAPIClient
import time

client = ScraperAPIClient('b84eb72339700a4b47310d5fae46e41b')

p_location = input("Enter location: ")
p_size = int(input("Enter size: "))
#search_range = float(input("Enter the range of your search: "))

#start_time = time.time()

geolocator = Nominatim(user_agent="MenShoesBershka.py")
location = geolocator.geocode(p_location)
print((location.latitude, location.longitude))

location_around_user = client.get("https://www.bershka.com/itxrest/2/bam/store/44009506/physical-store?latitude="+str(location.latitude)+"&longitude="+str(location.longitude)+"&countryCode=GB&max=10&appId=2&languageId=-1").json()

store_ids = []

x = 0

while x < len(location_around_user["closerStores"]):
    print(location_around_user["closerStores"][x]["id"]+", "+location_around_user["closerStores"][x]["name"])
    store_ids.append(location_around_user["closerStores"][x]["id"])
    x = x+1

products = client.get("https://www.bershka.com/itxrest/2/catalog/store/44009506/40259534/category/1010193202/product?languageId=-1").json()

i = 0

p_pn = []

while i < len(products["products"]):
    p_pn.append(products["products"][i]["bundleProductSummaries"][0]["detail"]["colors"][0]["sizes"][(p_size-5)]["partnumber"][0:13])
    print(p_pn[i]+" ", i+1)
    try:
        p_stock = client.get("https://itxrest.inditex.com/LOMOServiciosRESTCommerce-ws/common/1/stock/campaign/V2021/product/part-number/"+p_pn[i]+"?physicalStoreId="+store_ids[0]+"&physicalStoreId="+store_ids[1]+"&physicalStoreId="+store_ids[2]).json()
        #print(products["products"][i]["id"])
        counter = 0
        if "stocks" not in p_stock:
            print("product not available in stores around you.")
        else:
            while counter < len(p_stock["stocks"]):
                if not any(d["size"] == (34+p_size) for d in p_stock["stocks"][counter]["sizeStocks"]):
                    print("This store doesn't have your size: "+str(p_stock["stocks"][counter]["physicalStoreId"]))
                    # does not exist
                else:
                    print("Available at: "+str(p_stock["stocks"][counter]["physicalStoreId"]))
                counter = counter + 1
    except ValueError:
        print("product not available in stores around you")
    finally:
        i=i+1

#print("Process finished --- %s seconds ---" % round((time.time() - start_time),2))
