import requests
from bs4 import BeautifulSoup
import csv
from random import randint
from time import sleep

file = open('whiskeys.csv', 'w', encoding="utf-8", newline="\n")
file_object = csv.writer(file)
file_object.writerow(["სახელი", "ალკოჰოლის შემცველობა", "წარმოშობა", "სახეობა", "ფასი(₾)"])

page = 1
while page <= 5:
    url = f"https://alcorium-store.ge/%E1%83%95%E1%83%98%E1%83%A1%E1%83%99%E1%83%98-ka/page-{page}/"
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    content = soup.find("div", id="categories_view_pagination_contents")
    whiskeys = content.find_all("div", class_="ty-product-list clearfix")

    for whisky in whiskeys:
        name = whisky.bdi.a.text
        price = whisky.find("span", class_="ty-price-num").text
        product_features_html = whisky.find_all("span", class_="ty-control-group")
        data = {}
        for product in product_features_html:
            product_features = product.text
            if "ალკ. შემცველობა" in product_features:
                percentage = product_features[15:]
                data["percentage"] = percentage
            if "წარმოშობა" in product_features:
                origin = product_features[9:]
                data["origin"] = origin
            if "სახეობა" in product_features:
                species = product_features[7:]
                data["species"] = species
        file_object.writerow([name, data["percentage"], data["origin"], data["species"], price])
        print(name)
    sleep(randint(15, 20))
    page += 1



