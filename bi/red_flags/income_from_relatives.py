# We try to find declarations, where declarant has income from relative (source of income is one of the relatives)
# or some of the relatives receives income from declarant
# Unfortunately, analysis showed that vast majority of such cases are either are child-support payments (alimony), 
# and in this case the child is stated as income 'source'
# or these are just mistakes

import json
import re
import string
from bz2file import open as bzopen

matches_dataset = [] # we will save here urls of declarations which match our conditions

# download archive from here: https://declarations.com.ua/static/data/full_export.json.bz2
with bzopen("full_export.json.bz2", "rt", encoding = "utf8") as fp:
    for i, l in enumerate(fp):
        print i # just for understanding the process
        r = json.loads(l)
        if (not r['related_entities']['documents']['corrected']): # check that declaration was not corrected afterwards
            if (r['infocard']['document_type'] == unicode("Щорічна", "utf-8")): # look only for annual declarations
                if ('step_0' in r['unified_source'].keys()):
                    if (r['unified_source']['step_0']['declarationYear1'].encode("utf8") in ['2015', '2016', '2017']): # we use only declarations from these years to ensure that these are 'e-declarations', not paper ones

                        if "step_2" in r["unified_source"].keys(): # declarant has relatives
                            if "step_11" in r["unified_source"].keys(): # there is income reported
                        
                                # Save declarant name - full and processed
                                
                                decl_name = r["infocard"]["last_name"] + " " + r["infocard"]["first_name"] + " " + r["infocard"]["patronymic"]
                                decl_name = re.sub(' +', ' ', decl_name.lower().encode("utf8").translate(None, string.punctuation).strip())
                                
                                # List of family names in all types (ua, eng, current, previous)
                                
                                family_names = []
                                
                                for i in r["unified_source"]["step_2"].keys():
                                
                                    fn = r["unified_source"]["step_2"][i]["lastname"] + " " + r["unified_source"]["step_2"][i]["firstname"] + " " + r["unified_source"]["step_2"][i]["middlename"]
                                    fn = re.sub(' +', ' ', fn.lower().encode("utf8").translate(None, string.punctuation).strip())
                                    
                                    family_names.append(fn)
                                    
                                    if "previous_lastname" in r["unified_source"]["step_2"][i]:
                                        if r["unified_source"]["step_2"][i]["previous_lastname"].encode("utf-8") != "":
                                            fn = r["unified_source"]["step_2"][i]["previous_lastname"] + " " + r["unified_source"]["step_2"][i]["previous_firstname"] + " " + r["unified_source"]["step_2"][i]["previous_middlename"]
                                            fn = re.sub(' +', ' ', fn.lower().encode("utf8").translate(None, string.punctuation).strip())
                                            family_names.append(fn)
                                
                                    if "eng_lastname" in r["unified_source"]["step_2"][i]:
                                        if r["unified_source"]["step_2"][i]["eng_lastname"].encode("utf-8") != "":
                                            fn = r["unified_source"]["step_2"][i]["eng_lastname"] + " " + r["unified_source"]["step_2"][i]["eng_firstname"] + " " + r["unified_source"]["step_2"][i]["eng_middlename"]
                                            fn = re.sub(' +', ' ', fn.lower().encode("utf8").translate(None, string.punctuation).strip())
                                            family_names.append(fn)
                                            
                                    if "previous_eng_lastname" in r["unified_source"]["step_2"][i]:
                                        if r["unified_source"]["step_2"][i]["previous_eng_lastname"].encode("utf-8") != "":
                                            fn = r["unified_source"]["step_2"][i]["previous_eng_lastname"] + " " + r["unified_source"]["step_2"][i]["previous_eng_firstname"] + " " + r["unified_source"]["step_2"][i]["previous_eng_middlename"]
                                            fn = re.sub(' +', ' ', fn.lower().encode("utf8").translate(None, string.punctuation).strip())
                                            family_names.append(fn)
                                
                                del fn, i
                                
                                income_between_relatives = 0 # flag
                                
                                # Loop through income
                                for i in r["unified_source"]["step_11"].keys():
                                    check = 0
                                    
                                    # Should we check this income? If source is not a company, then yes
                                    if ("source_citizen" not in r["unified_source"]["step_11"][i].keys()):
                                        check = 1
                                    elif (not bool(re.search("Юридична особа", r["unified_source"]["step_11"][i]["source_citizen"].encode("utf-8")))):
                                        check = 1
                                    
                                    if (check == 1):
                                        if r["unified_source"]["step_11"][i]["person"] == '1': # if this is declarant's income
                                            
                                        # here we will check all options of income sources - if they are present in family_names
                                            if ("source_ua_lastname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["source_ua_lastname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["source_ua_lastname"] + " " + r["unified_source"]["step_11"][i]["source_ua_firstname"] + " " + r["unified_source"]["step_11"][i]["source_ua_middlename"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if s in family_names:
                                                        income_between_relatives = 1
                                                        break
                                            if ("ua_lastname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["ua_lastname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["ua_lastname"] + " " + r["unified_source"]["step_11"][i]["ua_firstname"] + " " + r["unified_source"]["step_11"][i]["ua_middlename"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if s in family_names:
                                                        income_between_relatives = 1
                                                        break
                                            if ("ukr_lastname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["ukr_lastname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["ukr_lastname"] + " " + r["unified_source"]["step_11"][i]["ukr_firstname"] + " " + r["unified_source"]["step_11"][i]["ukr_middlename"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if s in family_names:
                                                        income_between_relatives = 1
                                                        break
                                            if ("eng_lastname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["eng_lastname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["eng_lastname"] + " " + r["unified_source"]["step_11"][i]["eng_firstname"] + " " + r["unified_source"]["step_11"][i]["eng_middlename"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if s in family_names:
                                                        income_between_relatives = 1
                                                        break
                                            if ("source_ukr_fullname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["source_ukr_fullname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["source_ukr_fullname"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if s in family_names:
                                                        income_between_relatives = 1
                                                        break                           
                                            if ("source_eng_fullname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["source_ukr_fullname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["source_ukr_fullname"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if s in family_names:
                                                        income_between_relatives = 1
                                                        break
                                               
                                        else: # if this is income of the family
                                            # here we will check all options of income sources - if they match the name of the declarant
                                            if ("source_ua_lastname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["source_ua_lastname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["source_ua_lastname"] + " " + r["unified_source"]["step_11"][i]["source_ua_firstname"] + " " + r["unified_source"]["step_11"][i]["source_ua_middlename"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if (s == decl_name):
                                                        income_between_relatives = 1
                                                        break
                                            if ("ua_lastname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["ua_lastname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["ua_lastname"] + " " + r["unified_source"]["step_11"][i]["ua_firstname"] + " " + r["unified_source"]["step_11"][i]["ua_middlename"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if (s == decl_name):
                                                        income_between_relatives = 1
                                                        break
                                            if ("ukr_lastname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["ukr_lastname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["ukr_lastname"] + " " + r["unified_source"]["step_11"][i]["ukr_firstname"] + " " + r["unified_source"]["step_11"][i]["ukr_middlename"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if (s == decl_name):
                                                        income_between_relatives = 1
                                                        break
                                            if ("eng_lastname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["eng_lastname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["eng_lastname"] + " " + r["unified_source"]["step_11"][i]["eng_firstname"] + " " + r["unified_source"]["step_11"][i]["eng_middlename"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if (s == decl_name):
                                                        income_between_relatives = 1
                                                        break
                                            if ("source_ukr_fullname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["source_ukr_fullname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["source_ukr_fullname"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if (s == decl_name):
                                                        income_between_relatives = 1
                                                        break                           
                                            if ("source_eng_fullname" in r["unified_source"]["step_11"][i].keys()):
                                                if (r["unified_source"]["step_11"][i]["source_ukr_fullname"] != ""):
                                                    s = r["unified_source"]["step_11"][i]["source_ukr_fullname"]
                                                    s = s.lower().encode("utf8").translate(None, string.punctuation).strip()
                                                    if (s == decl_name):
                                                        income_between_relatives = 1
                                                        break
                        
                                del i, family_names, decl_name, check
                                
                        if (income_between_relatives == 1):
                            matches_dataset.append(r["infocard"]["url"]) # add urls of those who have income from relatives (or relatives has income from declarant)

