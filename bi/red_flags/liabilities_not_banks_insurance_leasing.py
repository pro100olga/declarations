import requests
import string
import re
import pandas as pd

####################### BANKS NAMES AND EDRPOU CODES

# We will take data about banks from 2 APIs (data.gov.ua and nbu.rocks) and extract EDRPOU codes and banks' names

banks1 = requests.get("http://data.gov.ua/sites/default/files/media//320/28.03.2018/05_Dovidnyk_bankiv_Ukrajiny_in_json.json").json()
banks2 = requests.get("http://nbu.rocks/jsons/complete.json").json()

banks1 = banks1['rcukru']['rowrcukru'] # extract list of banks

# Create a list of EDRPOU codes

banks_edrpou = []
banks_names = []

for i in range(len(banks1)): # add all codes from 1st list, convert them to single type - string

    # Long bank name (2 options - when it's in unicode or simple string)    
    if (isinstance(banks1[i]['FULLNAME'], unicode)):
        banks_names.append(re.sub(' +',' ', banks1[i]['FULLNAME'].lower().encode('utf8').translate(None, string.punctuation).strip())) # convert to string, remove all punctuation, double spaces and trail spaces, lowercase
    else:
        banks_names.append(re.sub(' +',' ', banks1[i]['FULLNAME'].lower().translate(None, string.punctuation).strip())) # remove all punctuation, double spaces and trail spaces, lowercase
   
    # Short bank name (2 options - when it's in unicode or simple string)    
    if (isinstance(banks1[i]['SHORTNAME'], unicode)):
        banks_names.append(re.sub(' +',' ', banks1[i]['SHORTNAME'].lower().encode('utf8').translate(None, string.punctuation).strip())) # convert to string, remove all punctuation, double spaces and trail spaces, lowercase
    else:
        banks_names.append(re.sub(' +',' ', banks1[i]['SHORTNAME'].lower().translate(None, string.punctuation).strip())) # remove all punctuation, double spaces and trail spaces, lowercase
    
    # EDRPOU code (2 options - when it's in unicode or simple string)    
    if (isinstance(banks1[i]['IKOD'], unicode)):
        banks_edrpou.append(banks1[i]['IKOD'].encode('utf8'))
    else:
        banks_edrpou.append(str(banks1[i]['IKOD']))


for i in range(len(banks2)): # add all codes from 2nd list, convert them to single type - string

    # Bank name (2 options - when it's in unicode or simple string)    
    if (isinstance(banks2[i]['Ліцензії'.decode("utf8")][0]['Назва банку'.decode("utf8")], unicode)):
        banks_names.append(re.sub(' +',' ', banks2[i]['Ліцензії'.decode("utf8")][0]['Назва банку'.decode("utf8")].lower().encode('utf8').translate(None, string.punctuation).strip())) # convert to string, remove all punctuation, double spaces and trail spaces, lowercase
    else:
        banks_names.append(re.sub(' +',' ', banks2[i]['Ліцензії'.decode("utf8")][0]['Назва банку'.decode("utf8")].lower().translate(None, string.punctuation).strip())) # remove all punctuation, double spaces and trail spaces, lowercase
   
    # EDRPOU code (2 options - when it's in unicode or simple string)    
    if (isinstance(banks2[i]['Ліцензії'.decode("utf8")][0]['Код ЄДРПОУ'.decode("utf8")], unicode)):
        banks_edrpou.append(banks2[i]['Ліцензії'.decode("utf8")][0]['Код ЄДРПОУ'.decode("utf8")].encode('utf8'))
    else:
        banks_edrpou.append(str(banks2[i]['Ліцензії'.decode("utf8")][0]['Код ЄДРПОУ'.decode("utf8")]))

del banks1, banks2, i
        
# Additional processing

banks_edrpou = list(set(banks_edrpou)) # remove duplicates EDRPOU codes
banks_edrpou = list(filter(None, banks_edrpou)) # remove empty strings
banks_edrpou = list(filter(lambda s: s not in ['0', 'None'], banks_edrpou)) # remove empty strings

# Now we will create all possible options of EDRPOU codes
# A code generally is 8 characters long and can start with zeros - then we will extract only non-zero characters and add them to the list
# Or it could be less than 8 characters - then we will add options with zeros in the beginning 
# We are not changing the existing values, but adding new ones

len_banks_edrpou = len(banks_edrpou)

for i in range(len_banks_edrpou):
    if len(banks_edrpou[i]) < 8:
        banks_edrpou.append('0'*(8-len(banks_edrpou[i])) + banks_edrpou[i])
    if ((len(banks_edrpou[i]) == 8) & (banks_edrpou[i][0] == '0')):
        banks_edrpou.append(banks_edrpou[i].lstrip('0'))     

del len_banks_edrpou, i

# We will add names of banks without all additional words

len_banks_names = len(banks_names)

for i in range(len_banks_names):
    if bool(re.search('філія|управління|пат|(публічне |)акціонерне товариство|(публічного |)акціонерного товариства|(а|)кб |акціонерний банк|^ат | ат ', \
                   banks_names[i])):
        banks_names.append(re.sub(' +', ' ', \
                                  re.sub('філія|управління|пат|(публічне |)акціонерне товариство|(публічного |)акціонерного товариства|(а|)кб |акціонерний банк|^ат | ат ', \
                                  '', banks_names[i])).strip())

banks_names = list(set(banks_names)) # remove duplicates of banks' names
banks_names = list(filter(None, banks_names)) # remove empty strings
banks_names = list(filter(lambda s: s not in ['0', 'None', 'банк', 'банки'], banks_names)) # remove empty strings and strings with just 'bank/s' word

del len_banks_names, i

####################### SEARCH PROCEDURE

# Read the whole list of declarations (this is just for the test)

decl_list = pd.read_csv("declarations_for_bi.csv", sep = ",", encoding = "utf8")

# Filter only those who have liabilities and keep only their ids (this is just for the test)

decl_list = decl_list[decl_list["liabilities.total"] > 0]["id"]

# Dataset to write results

d = pd.DataFrame({'id': [], 'emitent_code': [], 'emitent_name': [], 'object_type': [], 'object_other': [], 'reason': []})

# Loop through users who have liabilities, download their jsons and inspect them

for d_i in range(1000):

    r = requests.get("https://declarations.com.ua/declaration/" +  decl_list.iloc[d_i] + "?format=opendata").json()
    
    if ("step_13" in (r['declaration']['unified_source'].keys())): # check if there are liabilities
        
        for i in r['declaration']['unified_source']['step_13'].keys(): # loop thorigh liabilities in a particular declaration
            
            skip = 0 # should this liability be skipped (if it's a bank or the type of liability refers to insurance or leasing), this is only for the test
            reason = "" # what is the reason for not skippin (first conditions which is checked and met), this is only for the test
            
            # Check if type of liabilities refer to leasing or insurance
            
            if ("objectType" in r['declaration']['unified_source']['step_13'][i].keys()):
                if (bool(re.search(pattern = "лізинг", string = (re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["objectType"].lower().encode("utf8")))))
                or (bool(re.search(pattern = "пенсі", string = (re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["objectType"].lower().encode("utf8"))))))
                or (bool(re.search(pattern = "страхув", string = (re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["objectType"].lower().encode("utf8"))))))):
                    skip = 1
                    reason = "object type"
            
            if skip == 0: # if type of liabilities is not in leasing or insurance, we continue
                # we will check if "other type" field contains anything related to insurance or leasing
                if ("otherObjectType" in r['declaration']['unified_source']['step_13'][i].keys()):
                    if (bool(re.search(pattern = "л(і|и)зинг", string = (re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["otherObjectType"].lower().encode("utf8")))))
                    or (bool(re.search(pattern = "пенс(і|и)", string = (re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["otherObjectType"].lower().encode("utf8"))))))
                    or (bool(re.search(pattern = "страх(у|о)в", string = (re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["otherObjectType"].lower().encode("utf8"))))))):
                        skip = 1
                        reason = "other object type"
            
            if skip == 0: # if type of liabilities and "other type" is not in leasing or insurance, we continue
                # we will check if emitent of liability is a bank - by checking is its EDRPOU in the list of banks EDRPOU
                emitent_codes = [] #create a list of EDRPOU codes of emitent (we will check different elements of the list, as code could be mentioned in several elements of the json)
                
                if ("emitent_ua_company_code" in r['declaration']['unified_source']['step_13'][i].keys()):
                    if (isinstance(r['declaration']['unified_source']['step_13'][i]["emitent_ua_company_code"], unicode)):
                        emitent_codes.append(r['declaration']['unified_source']['step_13'][i]["emitent_ua_company_code"].encode('utf8'))
                    else:
                        emitent_codes.append(str(r['declaration']['unified_source']['step_13'][i]["emitent_ua_company_code"]))
                        
                if ("emitent_eng_company_code" in r['declaration']['unified_source']['step_13'][i].keys()):
                    if (isinstance(r['declaration']['unified_source']['step_13'][i]["emitent_eng_company_code"], unicode)):
                        emitent_codes.append(r['declaration']['unified_source']['step_13'][i]["emitent_eng_company_code"].encode('utf8'))
                    else:
                        emitent_codes.append(str(r['declaration']['unified_source']['step_13'][i]["emitent_eng_company_code"]))
                
                emitent_codes = list(set(emitent_codes)) # remove duplicates
                emitent_codes = list(filter(None, emitent_codes)) # remove empty strings
                emitent_codes = list(filter(lambda s: s not in ['0', 'None'], emitent_codes)) # remove empty strings
                      
                # check if this code is in the list with banks' codes
                for j in range(len(emitent_codes)):
                    if (emitent_codes[j] in banks_edrpou):
                        skip = 1
                        reason = "EDRPOU"
                        break
                
            if skip == 0: # if type of liabilities and "other type" is not in leasing or insurance, and emitent EDRPOU is not in list of banks' EDRPOU, we continue
                # we will check if emitent's name is in list of bank names
                emitent_names = [] #create a list of emitents' names (we will check different elements of the list, as name could be mentioned in several elements of the json)
                
                if ("emitent_ua_company_name" in r['declaration']['unified_source']['step_13'][i].keys()):
                    if (isinstance(r['declaration']['unified_source']['step_13'][i]["emitent_ua_company_name"], unicode)):
                        emitent_names.append(re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["emitent_ua_company_name"].lower().encode('utf8').translate(None, string.punctuation).strip()))
                    else:
                        emitent_names.append(re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["emitent_ua_company_name"].lower().translate(None, string.punctuation).strip()))
                        
                if ("emitent_ukr_company_name" in r['declaration']['unified_source']['step_13'][i].keys()):
                    if (isinstance(r['declaration']['unified_source']['step_13'][i]["emitent_ukr_company_name"], unicode)):
                        emitent_names.append(re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["emitent_ukr_company_name"].lower().encode('utf8').translate(None, string.punctuation).strip()))
                    else:
                        emitent_names.append(re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["emitent_ukr_company_name"].lower().translate(None, string.punctuation).strip()))
                        
                if ("emitent_eng_company_name" in r['declaration']['unified_source']['step_13'][i].keys()):
                    if (isinstance(r['declaration']['unified_source']['step_13'][i]["emitent_eng_company_name"], unicode)):
                        emitent_names.append(re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["emitent_eng_company_name"].lower().encode('utf8').translate(None, string.punctuation).strip()))
                    else:
                        emitent_names.append(re.sub(' +',' ', r['declaration']['unified_source']['step_13'][i]["emitent_eng_company_name"].lower().translate(None, string.punctuation).strip()))
                        
                emitent_names = list(set(emitent_names)) # remove duplicates
                emitent_names = list(filter(None, emitent_names)) # remove empty strings
                emitent_names = list(filter(lambda s: s not in ['0', 'None'], emitent_names)) # remove empty strings
                
                # check if any element of the banks names list occurs in the company names specified by user (full match is not required)
                for j in range(len(emitent_names)):
                    if any(bool(re.search(s, emitent_names[j])) for s in banks_names):
                        skip = 1
                        reason = "company name"
                        break
                    
                       
            # Add info to the dataframe, regardless if it was skipped or not (only for the test)
            d = d.append(pd.DataFrame(data = {'id': [decl_list.iloc[d_i]], 
                                              'emitent_code': [emitent_codes],
                                              'emitent_name': [emitent_names],
                                              'object_type':  [r['declaration']["unified_source"]["step_13"][i]["objectType"] if "objectType" in r['declaration']["unified_source"]["step_13"][i].keys() else ''],
                                              'object_other': [r['declaration']["unified_source"]["step_13"][i]["otherObjectType"] if "objectType" in r['declaration']["unified_source"]["step_13"][i].keys() else ''],
                                              'reason': [reason]}))

            
