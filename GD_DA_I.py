# ******************** Cocktail Recipe Extraction Process ********************


# load required packages

import requests
from bs4 import BeautifulSoup
import json
import timeit

# import pymongo

c_href = BeautifulSoup(requests.get('http://www.upneat.rocks/recipe/sources/death-co').text, 'html.parser'). \
    select('a[href^="/recipes/"]')

c_link = []
for link in c_href:
    c_link.append(link.get('href'))

c_name = []
for element in c_href:
    c_name.append(element.get_text())

c_data = []

for element, ele in zip(c_link, c_name):
    url = "http://www.upneat.rocks{}".format(element)
    c_url = BeautifulSoup(requests.get(url).text, 'html.parser')
    c_recipe = c_url.find('div', class_='col-md-12 col-lg-5'). \
        find('ul').get_text(',', strip=True).split(',')
    c_method_list = c_url.find('div', class_='col-md-12 col-lg-5'). \
        find('ul').next_sibling.next_sibling.get_text(strip=True).split('\n')
    c_method = ''.join(c_method_list)
    # c_create_list = c_url.find('div', class_='col-md-12 col-lg-5'). \
    #     find('ul').next_sibling.next_sibling.next_sibling.next_sibling.get_text(',', strip=True).split(',')
    # c_create = ''.join(c_create_list)
    # c_creator = c_create_list[0].strip()
    # c_year = c_create_list[1].strip()
    c_data.append(
        {"cocktail": ele, "source": url, "ingredient": c_recipe, "method": c_method})


test = json.dumps(c_data)
print(test)

# def data_to_mongo(c_data):
# client = pymongo.MongoClient("mongodb://m001-student:m001-mongodb-basics@m001-sandbox-shard-00-00-rdhhd.mongodb.net:27017,m001-sandbox-shard-00-01-rdhhd.mongodb.net:27017,m001-sandbox-shard-00-02-rdhhd.mongodb.net:27017/test?ssl=true&replicaSet=m001-sandbox-shard-0&authSource=admin")
# db = client.cocktail
# col = db.recipe
# result = col.insert_many(c_data)
# pprint(result)
