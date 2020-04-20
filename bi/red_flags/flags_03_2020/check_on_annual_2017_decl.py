decl_folder = "" # working dir

import pandas as pd
import json
import datetime
import numpy as np

pd.set_option('display.max_columns', None)


def getListOfFiles(dirName):
    
    """
    Function gets list of all declarations, downloaded from data.gov.ua
    """
    
    import os
    
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles


annual_2017_decl_list = getListOfFiles("C:\\Users\\olga.makarova\\Downloads\\declarations\\2018_tar\\2018\\")
# # insert here directory with jsons from here https://data.gov.ua/dataset/e030e5cc-f28b-43eb-aab4-6d1940ed7699

#
# Read aggregated file with all flags and filter only those declarations to check with jsons
#

decl_folder = "C:\\Users\\olga.makarova\\Downloads\\declarations\\"

d = pd.read_csv(decl_folder + "aggregated_with_flags.csv")

df = d[(d['year'] == 2017) & (d['doc_type'] == "Щорічна")]

# df.to_csv("C:\\Users\\olga.makarova\\Downloads\\declarations\\annual_2017_decl.csv")

del d

df_full = df

# df = df_full.iloc[:50000,]

df = df_full.sample(n = 500000, replace = False, random_state = 10)

ids_set = set(df['id'])

# Read exchange rates data for liabilities check

exchange_rates_df = pd.read_csv(decl_folder + "exchange_rates.csv")
exchange_rates_df = exchange_rates_df.iloc[:,0:3]
exchange_rates_df.columns = ["currency_code", "year", "exchange_rate"]

#
# CHECK
# 

result_dict = {}
mismatches = 0
i = 0

for json_fname in annual_2017_decl_list:
    
    #print(json_fname)
   
    if i % 5000 == 0:      
        print(str(i) + ": " + str(datetime.datetime.now()))
        
        #if mismatches > 0:
         #   print("Number of mismatches: " + str(mismatches))
        
    
    if "nacp_" + json_fname[66:-5] in ids_set:
        
        
        with open(json_fname, encoding="utf8") as json_file:
            
            decl = json.load(json_file)
            
            decl_df_row = df[df['id'] == "nacp_" + decl['id']]
            
            # liabilities
            
            (liab_total, liab_flag) = flag_liabilities_to_inc_and_assets(decl = decl,
                                                                        income_and_assets_sum = decl_df_row[['assets.total', 'incomes.total']].sum(axis = 1).values[0], 
                                                                        exchange_rates_df = exchange_rates_df)
            
            total_liabilities_match_value = liab_total - decl_df_row['liabilities.total'] == 0
            total_liabilities_match_value = total_liabilities_match_value.values[0]
            
            #flag_liabilities_to_inc_and_assets_value = liab_flag == decl_df_row['family_member_did_not_provide_information']
            #flag_liabilities_to_inc_and_assets_value = flag_liabilities_to_inc_and_assets_value.values[0]
            
            result_dict[decl['id']] = {#CLOSED 'flag_corp_rights_abroad': flag_corp_rights_abroad(decl, ans = decl_df_row['corprights_abroad_flag'].values), 
                                       #'flag_estate_has_hidden_cost': flag_estate_has_hidden_cost(decl, ans = decl_df_row['estate_has_hidden_cost'].values),
                                       'flag_has_huge_prize': flag_has_huge_prize(decl, ans = decl_df_row['has_huge_prize'].values),
                                       'flag_has_aircraft': flag_has_aircraft(decl, ans = decl_df_row['has_aircraft_flag'].values),
                                       'flag_has_major_real_estate': flag_has_major_real_estate(decl, ans = decl_df_row['has_major_real_estate'].values),
                                       'flag_has_foreign_real_estate': flag_has_foreign_real_estate(decl, ans = decl_df_row['has_foreign_real_estate'].values),
                                        #CLOSED'flag_has_bo_abroad': flag_has_bo_abroad(decl, ans = decl_df_row['has_bo_abroad'].values), 
                                       'flag_has_non_bank_liabilities': flag_has_non_bank_liabilities(decl, ans = decl_df_row['has_non_bank_liabilities'].values),
                                       'flag_vehicle_purch_no_cost': flag_vehicle_purch_no_cost(decl, ans = decl_df_row['vehicle_purch_no_cost_flag'].values),
                                       'flag_estate_purch_no_cost': flag_estate_purch_no_cost(decl, ans = decl_df_row['estate_purch_no_cost_flag'].values),
                                       'flag_family_member_did_not_provide_information': flag_family_member_did_not_provide_information(decl, 
                                                                                                                                        ans = decl_df_row['family_member_did_not_provide_information'].values)
                                       #'total_liabilities_match': total_liabilities_match_value,
                                       #'flag_liabilities_to_inc_and_assets': flag_liabilities_to_inc_and_assets_value
                                       }
    
            #mismatches = mismatches + print_check_result(func_name = "flag_corp_rights_abroad", flag_col_name = "corprights_abroad_flag", i = i)           
            # mismatches = mismatches + print_check_result(func_name = "flag_estate_has_hidden_cost", flag_col_name = "estate_has_hidden_cost", i = i)            
            #mismatches = mismatches + print_check_result(func_name = "flag_has_huge_prize", flag_col_name = "has_huge_prize", i = i)
            #mismatches = mismatches + print_check_result(func_name = "flag_has_aircraft", flag_col_name = "has_aircraft_flag", i = i)            
            # mismatches = mismatches + print_check_result(func_name = "flag_has_major_real_estate", flag_col_name = "has_major_real_estate", i = i)            
            # mismatches = mismatches + print_check_result(func_name = "flag_has_foreign_real_estate", flag_col_name = "has_foreign_real_estate", i = i)            
            # mismatches = mismatches + print_check_result(func_name = "flag_has_bo_abroad", flag_col_name = "has_bo_abroad", i = i)            
            # mismatches = mismatches + print_check_result(func_name = "flag_has_non_bank_liabilities", flag_col_name = "has_non_bank_liabilities", i = i)           
            #if mismatches > 0:
             #   break
            
    i = i + 1
        

result_pd = pd.DataFrame.from_dict(result_dict, orient = "index")
result_pd.to_csv(decl_folder + "result_pd.csv")

del i
del decl_df_row
del decl
del json_fname
del mismatches
del liab_flag
del liab_total
del total_liabilities_match_value
del flag_liabilities_to_inc_and_assets_value

for col in ['flag_has_huge_prize', 'flag_has_aircraft',
       'flag_has_major_real_estate', 'flag_has_foreign_real_estate',
       'flag_has_non_bank_liabilities', 'flag_vehicle_purch_no_cost',
       'flag_estate_purch_no_cost',
       'flag_family_member_did_not_provide_information'
       ]: # result_pd.columns:
    print(result_pd[col].value_counts())
    
del col
