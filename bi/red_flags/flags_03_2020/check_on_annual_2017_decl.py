decl_folder = "" # working dir

import pandas as pd
import json
import datetime

d = pd.read_csv(decl_folder + "aggregated_with_flags.csv")

df = d[(d['year'] == 2017) & (d['doc_type'] == "Щорічна")]

del d

ids_set = set(df['id'])

# annual_2017_decl_list = getListOfFiles() # insert here directory with jsons from here https://data.gov.ua/dataset/e030e5cc-f28b-43eb-aab4-6d1940ed7699

result_dict = {}
mismatches = 0
i = 0

for json_fname in annual_2017_decl_list:
   
    if i % 5000 == 0:      
        print(str(i) + ": " + str(datetime.datetime.now()))
        
        if mismatches > 0:
            print("Number of mismatches: " + str(mismatches))
        
    
    if "nacp_" + json_fname[66:-5] in ids_set:
    
        with open(json_fname, encoding="utf8") as json_file:
            
            decl = json.load(json_file)
            
            decl_df_row = df[df['id'] == "nacp_" + decl['id']]
            result_dict[decl['id']] = {'flag_corp_rights_abroad': flag_corp_rights_abroad(decl, ans = decl_df_row['corprights_abroad_flag'].values),
                                                   'flag_estate_has_hidden_cost': flag_estate_has_hidden_cost(decl, ans = decl_df_row['estate_has_hidden_cost'].values),
                                                   'flag_has_huge_prize': flag_has_huge_prize(decl, ans = decl_df_row['has_huge_prize'].values),
                                                   'flag_has_aircraft': flag_has_aircraft(decl, ans = decl_df_row['has_aircraft_flag'].values),
                                                   'flag_has_major_real_estate': flag_has_major_real_estate(decl, ans = decl_df_row['has_major_real_estate'].values),
                                                   'flag_has_foreign_real_estate': flag_has_foreign_real_estate(decl, ans = decl_df_row['has_foreign_real_estate'].values),
                                                   'flag_has_bo_abroad': flag_has_bo_abroad(decl, ans = decl_df_row['has_bo_abroad'].values),
                                                   'flag_has_non_bank_liabilities': flag_has_non_bank_liabilities(decl, ans = decl_df_row['has_non_bank_liabilities'].values)}
    
            mismatches = mismatches + print_check_result(func_name = "flag_corp_rights_abroad", flag_col_name = "corprights_abroad_flag", i = i)
            
            # mismatches = mismatches + print_check_result(func_name = "flag_estate_has_hidden_cost", flag_col_name = "estate_has_hidden_cost", i = i)
            
            mismatches = mismatches + print_check_result(func_name = "flag_has_huge_prize", flag_col_name = "has_huge_prize", i = i)
            
            mismatches = mismatches + print_check_result(func_name = "flag_has_aircraft", flag_col_name = "has_aircraft_flag", i = i)
            
            # mismatches = mismatches + print_check_result(func_name = "flag_has_major_real_estate", flag_col_name = "has_major_real_estate", i = i)
            
            mismatches = mismatches + print_check_result(func_name = "flag_has_foreign_real_estate", flag_col_name = "has_foreign_real_estate", i = i)
            
            mismatches = mismatches + print_check_result(func_name = "flag_has_bo_abroad", flag_col_name = "has_bo_abroad", i = i)
            
            # mismatches = mismatches + print_check_result(func_name = "flag_has_non_bank_liabilities", flag_col_name = "has_non_bank_liabilities", i = i)
            
            #if mismatches > 0:
             #   break
            
    i = i + 1
        

result_pd = pd.DataFrame.from_dict(result_dict, orient = "index")
result_pd.to_csv(decl_folder + "result_pd.csv")
        
print(result_dict)

del i
del decl_df_row
del decl
del json_fname

for col in result_pd.columns:
    print(result_pd[col].value_counts())
    
del col
