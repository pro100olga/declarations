import pandas as pd
import json
from bz2file import open as bzopen

### Check if list is essentially empty 
### https://stackoverflow.com/questions/1593564/python-how-to-check-if-a-nested-list-is-essentially-empty

def isListEmpty(inList):
    if isinstance(inList, list): # Is a list
        return all( map(isListEmpty, inList) )
    return False # Not a list

### Create list with results

people_and_companies = pd.DataFrame({'id': [], 'person': [], 'relation_type': [], 
                                     'fio': [], 'office': [], 'position': [],
                                     'document_type': [], 'app_date': [],
                                     'company_ua': [], 'company_id': [], 'company_name': []})


#import requests 
#r = requests.get("https://declarations.com.ua/declaration/nacp_9ec0dc59-76ae-486b-a1ce-f0fdc82169f4?format=opendata").json()
#r = r['declaration']
    
### Archive with all declarations: https://declarations.com.ua/static/data/full_export.json.bz2

with bzopen("full_export.json.bz2", "rt", encoding = "utf8") as fp:
    for i, l in enumerate(fp):
        print(str(i))
        r = json.loads(l) # load one declaration
        if 'declaration' in r.keys():
            r = r['declaration']
        
        if (not r['related_entities']['documents']['corrected']): # check that this declaration was not corrected afterwards
            if r['infocard']['source'] == 'NACP':
               
                result_list = []
                
                if (r['infocard']['document_type'] == "Щорічна"): 
                    if (r['unified_source']['step_0']['declarationYear1'] == "2017"): 
                        
                        # 7 Цінні папери
                        if ("step_7" in r['unified_source'].keys()):
                            if (not isListEmpty(r['unified_source']['step_7'])):
                                for i in r['unified_source']['step_7'].keys():
                                    company_id = ''
                                    company_name = ''
                                    if ('emitent_ua_company_code' in r['unified_source']['step_7'][i].keys()):
                                        if (r['unified_source']['step_7'][i]['emitent_ua_company_code'] != ''):
                                            company_id = r['unified_source']['step_7'][i]['emitent_ua_company_code']
                                            company_name = r['unified_source']['step_7'][i]['emitent_ua_company_name']
                                            company_ua = 1
                                    if company_id == '':
                                        if ('emitent_eng_company_code' in r['unified_source']['step_7'][i].keys()):
                                            if (r['unified_source']['step_7'][i]['emitent_eng_company_code'] != ''):
                                                company_id = r['unified_source']['step_7'][i]['emitent_eng_company_code']
                                                company_name = r['unified_source']['step_7'][i]['emitent_eng_company_name']
                                                company_ua = 0
                                    result_list.append(pd.DataFrame([{'id': r['infocard']['id'], 
                                                                                                     'person': r['unified_source']['step_7'][i]['person'],
                                                                                                     'relation_type': 7, 
                                                                                                     'fio': r['infocard']['last_name'] + ' ' + r['infocard']['first_name'] + ' ' + r['infocard']['patronymic'], 
                                                                                                    'office': r['infocard']['office'], 
                                                                                                    'position': r['infocard']['position'],
                                                                                                    'document_type': r['infocard']['document_type'], 
                                                                                                    'app_date': r['unified_source']['step_0']['declarationYear1'],
                                                                                                     'company_ua': company_ua,
                                                                                                     'company_id': company_id, 
                                                                                                     'company_name': company_name}]))
                        
                        # 8 Corporate rights
                        if ("step_8" in r['unified_source'].keys()):
                            if (not isListEmpty(r['unified_source']['step_8'])):
                                for i in r['unified_source']['step_8'].keys():
                                    company_id = ''
                                    company_name = ''
                                    if ('name' in r['unified_source']['step_8'][i].keys()):
                                        if (r['unified_source']['step_8'][i]['name'] != ''):
                                            company_name = r['unified_source']['step_8'][i]['name']
                                    if company_name == '':
                                        if ('en_name' in r['unified_source']['step_8'][i].keys()):
                                            if (r['unified_source']['step_8'][i]['en_name'] != ''):
                                                company_name = r['unified_source']['step_8'][i]['en_name']
                                    if r['unified_source']['step_8'][i]['country'] == '1':
                                        company_ua = 1
                                    else:
                                        company_ua = 0
                                    if ('corporate_rights_company_code' in r['unified_source']['step_8'][i].keys()):
                                        company_id = r['unified_source']['step_8'][i]['corporate_rights_company_code']
                                    result_list.append(pd.DataFrame([{'id': r['infocard']['id'], 
                                                                                                     'person': r['unified_source']['step_8'][i]['person'],
                                                                                                     'relation_type': 8, 
                                                                                                     'fio': r['infocard']['last_name'] + ' ' + r['infocard']['first_name'] + ' ' + r['infocard']['patronymic'], 
                                                                                                     'office': r['infocard']['office'], 
                                                                                                     'position': r['infocard']['position'],
                                                                                                     'document_type': r['infocard']['document_type'], 
                                                                                                     'app_date': r['unified_source']['step_0']['declarationYear1'],
                                                                                                     'company_ua': company_ua,
                                                                                                     'company_id': company_id, 
                                                                                                     'company_name': company_name}]))
                        
                        # 9 Бенефіціар, власник
                        if ("step_9" in r['unified_source'].keys()):
                            if (not isListEmpty(r['unified_source']['step_9'])):
                                for i in r['unified_source']['step_9'].keys():
                                    company_id = ''
                                    company_name = ''
                                    if ('name' in r['unified_source']['step_9'][i].keys()):
                                        if (r['unified_source']['step_9'][i]['name'] != ''):
                                            company_name = r['unified_source']['step_9'][i]['name']
                                    if company_name == '':
                                        if ('en_name' in r['unified_source']['step_9'][i].keys()):
                                            if (r['unified_source']['step_9'][i]['en_name'] != ''):
                                                company_name = r['unified_source']['step_9'][i]['en_name']
                                    if r['unified_source']['step_9'][i]['country'] == '1':
                                        company_ua = 1
                                    else:
                                        company_ua = 0
                                    if ('beneficial_owner_company_code' in r['unified_source']['step_9'][i].keys()):
                                        company_id = r['unified_source']['step_9'][i]['beneficial_owner_company_code']
                                    result_list.append(pd.DataFrame([{'id': r['infocard']['id'], 
                                                                                                     'person': r['unified_source']['step_9'][i]['person'],
                                                                                                     'relation_type': 9, 
                                                                                                     'fio': r['infocard']['last_name'] + ' ' + r['infocard']['first_name'] + ' ' + r['infocard']['patronymic'], 
                                                                                                    'office': r['infocard']['office'], 
                                                                                                    'position': r['infocard']['position'],
                                                                                                    'document_type': r['infocard']['document_type'], 
                                                                                                    'app_date': r['unified_source']['step_0']['declarationYear1'],
                                                                                                     'company_ua': company_ua,
                                                                                                     'company_id': company_id, 
                                                                                                     'company_name': company_name}]))
                                   
                        if (len(result_list) > 0):
                            people_and_companies = people_and_companies.append(result_list)

# Save resulting dataframe to csv
people_and_companies.to_csv("people_and_companies_7_8_9.csv", sep = "|", encoding = "utf-8")


