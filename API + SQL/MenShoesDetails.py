import requests
import json
import mysql.connector

"""mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="*******",
  database="test"
)"""

f = open("MenShoesLinks_API.txt")
lines = f.readlines()
f.close()

p_location = input("Enter location: ")
p_size = int(input("Enter size: "))
search_range = float(input("Enter the range of your search: "))

"""location = requests.get("https://www.riverisland.com/api/stores/inventorysearch?ProductId=397161&Query="+p_location+"&Type=FreeText&ShowOutOfStockStores=false&VariantId="+str(15324 + p_size)+"&page=1")

with open('menshoesAPI_locations.json', 'w') as f:
    json.dump(location.json(), f, indent = 4, sort_keys = True)"""

#for line in lines:
"""result = requests.get("https://api.riverisland.com/graphql?operationName=dressipiProduct&variables=%7B%22productId%22%3A%22"+line+"%22%2C%22countryCode%22%3A%22GB%22%2C%22currencyCode%22%3A%22GBP%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2230829bbeac07859fc4def17e98ca38c701da60a4ecea95a783c7525130e95e55%22%7D%7D")

    with open('menshoesAPI.json', 'w') as f:
        json.dump(result.json(), f, indent = 4, sort_keys = True)"""

    #location = requests.get("https://www.riverisland.com/api/stores/inventorysearch?ProductId="+line[0:6]+"&Query="+p_location+"&Type=FreeText&ShowOutOfStockStores=false&VariantId="+str(15324 + p_size)+"&page=1")
location = requests.get("https://www.riverisland.com/api/stores/inventorysearch?ProductId=316762&Query="+p_location+"&Type=FreeText&ShowOutOfStockStores=false&VariantId="+str(15324 + p_size)+"&page=1")

with open('menshoesAPI_locations.json', 'w') as f:
    json.dump(location.json(), f, indent = 4, sort_keys = True)

with open('menshoesAPI_locations.json') as json_file:
    data = location.json()

    """print("Locations of product " + line[0:6] + " around " + p_location + ":")
    if data["data"]["stores"] == []:
        print("No location found for this product.")
    else:
        for i in data["data"]["stores"]:
            if i["distanceFromOrigin"] < search_range:
                print(i["storeName"])
            else:
                print("Product out of range.")"""

"""sql = "INSERT INTO loca_prod (product_name, product_location, qty) VALUES (%s, %s, %s)"
val = (prod_name, prod_loc, prod_qty)
mycursor.execute(sql, val)

mydb.commit()"""