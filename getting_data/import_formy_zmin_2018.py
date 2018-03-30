# code example taken from here: https://declarations.com.ua/api/

import requests
import json
from time import sleep

data = []

print("Fetching page #%s" % 1)

# You can download other documents, the result of any search, see details here: https://declarations.com.ua/api/

r = requests.get("https://declarations.com.ua/search?q=&declaration_year=2018&doc_type=Форма+змін&format=opendata").json()
data += r["results"]["object_list"]

for page in range(2, r["results"]["paginator"]["num_pages"] + 1):
    sleep(0.5)
    print("Fetching page #%s" % page)

    subr = requests.get(
        "https://declarations.com.ua/search?q=&declaration_year=2018&doc_type=Форма+змін&format=opendata&page=%s" % page).json()
    data += subr["results"]["object_list"]

print("Declarations exported %s" % len(data))
with open("feed18.json", "w") as fp:
    json.dump(data, fp)

# To further parse this data, look here (code in R!): 
# https://github.com/pro100olga/declarations/blob/master/getting_data/process_data_from_formy_zmin.R
