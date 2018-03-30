import requests
import json
import pandas as pd

# csv is available here: https://declarations.com.ua/static/data/declarations_for_bi.csv.bz2
# these are aggregated and cleaned data, where one row is one declaration
# data is used for https://declarations.com.ua/BI/

d = pd.read_csv("declarations_for_bi.csv", encoding = "utf-8", sep = ",")

# You can filter the data by any available field
# Here we use annual declarations from 2016 (all declarations in the files are annual),
# but you may, for example, filter those from a separate region, organization, with certain amount of income, etc
# Dataset description is available here: 
# https://docs.google.com/spreadsheets/d/1gkimFwc9g-Yi3HvdrA5lh8iQZ6tqIJnG3dLBIgnUmqY/edit?usp=sharing

d = d[d['year'] == 2016]['id']
d = pd.DataFrame(d)
d = d.set_index([range(0, d['id'].size)])

# For all the files we need, download and save them

for i in range(0, d.shape[0]):
    print i # this is just to understand the progress
    
    # here we download the data from the site, but you can also save files localy and then access them
    # so that not to save all the files (tens of Gb), you may first save some of them using these code:
    # https://github.com/pro100olga/declarations/blob/master/getting_data/import_from_archive_and_save_as_jsons_with_conditions.py
    r = requests.get("http://declarations.com.ua/declaration/" + d.iloc[i]['id'] + "?format=opendata").json()
    
    with open("/jsons/" + d.iloc[i]['id'] + ".json", "w") as fp: # save the file
        json.dump(r, fp)
    
