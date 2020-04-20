"""
Functions used to check new flags for BI
"""

def print_check_result(func_name, flag_col_name, i):
    
    if not eval(func_name)(decl, ans = decl_df_row[flag_col_name].values):
        print(str(i) + ", " + func_name + " mismatch: " + decl['id'] + ", answer is " + str(decl_df_row[flag_col_name].values))
        return 1
    else:
        return 0
    
def str_to_float(s):
    import re
    if len(s) > 0:
        return float(re.sub(string = s, pattern = ",", repl = "."))
    else:
        return 0

def flag_corp_rights_abroad(decl, ans):
    
    # https://github.com/excieve/dragnet/issues/24
          
    flag = False
    
    if 'empty' not in set(decl['data']['step_8'].keys()):
   
        for k in decl['data']['step_8'].keys():
            
            if decl['data']['step_8'][k]['country'] not in ['', '1']:
                
                flag = True
                break
        
    return flag == ans        



def flag_estate_has_hidden_cost(decl, ans):
    
    # https://github.com/excieve/dragnet/issues/22
    
    import datetime
    
    flag = False
    
    if 'empty' not in set(decl['data']['step_3'].keys()):
        
        for k in decl['data']['step_3'].keys():
            
            if len(decl['data']['step_3'][k]['owningDate']) == 10:
                
                if int(decl['data']['step_3'][k]['owningDate'][6:]) > 0:
            
                    if datetime.datetime.strptime(decl['data']['step_3'][k]['owningDate'], "%d.%m.%Y").year + 5 >= str_to_float(decl['data']['step_0']['declarationYear1']):
                    
                        if str(decl['data']['step_3'][k]['costDate']) in ['', '0']:
                            
                            if str(decl['data']['step_3'][k]['costAssessment']) in ['', '0']:        
                                
                                for right in decl['data']['step_3'][k]['rights'].keys():
                                    
                                    declarant_and_family = list(decl['data']['step_2'].keys()) + ['1'] if isinstance(decl['data']['step_2'], dict) else ['1']
        
                                    if right in declarant_and_family:
                                    
                                        if decl['data']['step_3'][k]['rights'][right]['ownershipType'] in ['Власність', 'Спільна власність']:
                                                        
                                            flag = True
                                            break
            
    return flag == ans   

def flag_has_huge_prize(decl, ans):
    
    import re
    
    # https://github.com/excieve/dragnet/issues/37
    
    flag = False
    
    prize_amount = 0.0
    
    if 'empty' not in set(decl['data']['step_11'].keys()):
        
        for k in decl['data']['step_11'].keys():
            
            if decl['data']['step_11'][k]['objectType'] == "Приз":
                
                prize_amount = prize_amount + str_to_float(s = decl['data']['step_11'][k]['sizeIncome'])
            
            elif decl['data']['step_11'][k]['objectType'] == "Інше":
                
                if bool(re.search(string = decl['data']['step_11'][k]['otherObjectType'].lower(), 
                                  pattern = "вигра|лотере|мегалот|суперлото|призові|призи|призів")):
                    
                    prize_amount = prize_amount + str_to_float(s = decl['data']['step_11'][k]['sizeIncome'])
             
    if prize_amount >= 10000.0:
        flag = True        
    
    return flag == ans


def flag_has_aircraft(decl, ans):
    
    # https://github.com/excieve/dragnet/issues/39
    
    flag = False
    
    if 'empty' not in set(decl['data']['step_6'].keys()):
        
        for k in decl['data']['step_6'].keys():
            
            if decl['data']['step_6'][k]['objectType'] == "Повітряний засіб":
                
                flag = True
                break
            
    return flag == ans   



def flag_has_major_real_estate(decl, ans):
    
    # https://github.com/excieve/dragnet/issues/40
    
    import re
    
    flag = False
    
    if 'empty' not in set(decl['data']['step_3'].keys()):
        
        for k in decl['data']['step_3'].keys():
            
            if decl['data']['step_3'][k]['objectType'] in [ #'Інше',
                                                         #'Гараж',
                                                         'Житловий будинок',
                                                         #'Земельна ділянка',
                                                         'Квартира',
                                                         'Кімната',
                                                         #'Офіс',
                                                         'Садовий (дачний) будинок']:
            
                if len(decl['data']['step_3'][k]['totalArea']) > 0:
                
                    if str_to_float(s = decl['data']['step_3'][k]['totalArea']) > 300:
                                               
                        flag = True
                        break
            
    return flag == ans   


def flag_has_foreign_real_estate(decl, ans):
    
    # https://github.com/excieve/dragnet/issues/41
    
    flag = False
    
    if 'empty' not in set(decl['data']['step_3'].keys()):
        
        for k in decl['data']['step_3'].keys():
            
            if decl['data']['step_3'][k]['country'] not in  ["1", ""]:
                
                for right in decl['data']['step_3'][k]['rights'].keys():
                    
                    declarant_and_family = list(decl['data']['step_2'].keys()) + ['1'] if isinstance(decl['data']['step_2'], dict) else ['1']
        
                    if right in declarant_and_family:
                                    
                        if decl['data']['step_3'][k]['rights'][right]['ownershipType'] in ['Власність', 'Спільна власність', "Власником є третя особа"]:
                
                            flag = True
                            break
            
    return flag == ans   


def flag_has_bo_abroad(decl, ans):
    
    # https://github.com/excieve/dragnet/issues/42
    
    flag = False
    
    if 'empty' not in set(decl['data']['step_9'].keys()):
        
        for k in decl['data']['step_9'].keys():
            
            if decl['data']['step_9'][k]['country'] not in ["1", ""]:
                
                flag = True
                break
            
    return flag == ans   


def flag_has_non_bank_liabilities(decl, ans):
    
    import re
    
    # https://github.com/excieve/dragnet/issues/38
    
    # Load file - created by code from here 
    # https://github.com/pro100olga/declarations/blob/master/bi/red_flags/liabilities_not_banks_insurance_leasing.py
    
    banks_edrpou = pd.read_csv("banks_edrpou.csv")
    banks_edrpou = set(banks_edrpou['banks_edrpou'])
    
    banks_names = set(["твбв",
        "ощадбанк",
        "приватбанк",
        "аваль",
        "райффайзен",
        "абанк",
        "агріколь",
        "укрсиббанк",
        "альфабанк",
        "альфа банк",
        "альфа-банк",
        "пумб",
        "укргазбанк",
        "мегабанк",
        "акордбанк",
        "сбербанк",
        "таскомбанк",
        "кредобанк",
        "індустріалбанк",
        "укрексімбанк",
        "радабанк",
        "укркомунбанк",
        "укрбудінвестбанк",
        "правексбанк",
        "правекс",
        "прокредит",
        "метабанк",
        "комінвестбанк",
        "форвард",
        "дельта-банк",
        "дельтабанк",
        "укрсоцбанк",
        "дельта банк"])
    
    flag = False
            
    if 'empty' not in set(decl['data']['step_13'].keys()):
        
        for k in decl['data']['step_13'].keys():
            
            flag_company_code = False
            flag_ua_company_name = False
            flag_ukr_company_name = False
            flag_insurance_leasing_pension = False
            
            if bool(re.search(string = decl['data']['step_13'][k]['objectType'].lower(),
                              pattern = "страх|пенс|л[і|и]з[і|и]нг")):
                
                flag_insurance_leasing_pension = True
                
            if bool(re.search(string = decl['data']['step_13'][k]['otherObjectType'].lower(),
                              pattern = "страх|пенс|л[і|и]з[і|и]нг")):
                
                flag_insurance_leasing_pension = True
            
            if 'emitent_ua_company_code' in decl['data']['step_13'][k].keys():
                
                if len(decl['data']['step_13'][k]['emitent_ua_company_code']) > 0:
                
                    if int(decl['data']['step_13'][k]['emitent_ua_company_code']) in banks_edrpou:
                        
                        flag_company_code = True
                
           
            if 'emitent_ua_company_name' in decl['data']['step_13'][k].keys():
                
                if len(decl['data']['step_13'][k]['emitent_ua_company_name']) > 0:
                
                    banks_names_coincidences = 0
                    
                    for bank_name in banks_names:
                        
                        if bool(re.search(pattern = bank_name,
                                          string = decl['data']['step_13'][k]['emitent_ua_company_name'].lower())):
                            
                            banks_names_coincidences = 1
                            break
                        
                    if banks_names_coincidences == 1:
                        flag_ua_company_name = True
                        
                    
            if 'emitent_ukr_company_name' in decl['data']['step_13'][k].keys():
                
                if len(decl['data']['step_13'][k]['emitent_ukr_company_name']) > 0:
                
                    banks_names_coincidences = 0
                    
                    for bank_name in banks_names:
                        
                        if bool(re.search(pattern = bank_name,
                                          string = decl['data']['step_13'][k]['emitent_ukr_company_name'].lower())):
                            
                            banks_names_coincidences = 1
                            break
                        
                    if banks_names_coincidences == 1:
                        flag_ukr_company_name = True
                        
                    
            if not flag_company_code and not flag_ua_company_name and not flag_ukr_company_name and not flag_insurance_leasing_pension == True:
                break

        if not flag_company_code and not flag_ua_company_name and not flag_ukr_company_name and not flag_insurance_leasing_pension  == True:
            flag = True
        
    return  flag == ans



def flag_family_member_did_not_provide_information(decl, ans):
    
    # https://github.com/excieve/dragnet/issues/36
    
    flag = False
    
    fields_names_to_check = set(['addition_firstname_extendedstatus',
                            'addition_lastname_extendedstatus',
                            'amount_extendedstatus',
                            'assetsCurrency_extendedstatus',
                            'brand_extendedstatus',
                            'costAssessment_extendedstatus',
                            'costDateOrigin_extendedstatus',
                            'costDateUse_extendedstatus',
                            'costDate_extendedstatus',
                            'cost_extendedstatus',
                            'cost_percent_extendedstatus',
                            'country_extendedstatus',
                            'dateUse_extendedstatus',
                            'descriptionObject_extendedstatus',
                            'emitent_eng_company_name_extendedstatus',
                            'emitent_eng_fullname_extendedstatus',
                            'emitent_extendedstatus',
                            'emitent_ua_company_name_extendedstatus',
                            'emitent_ua_fullname_extendedstatus',
                            'emitent_ukr_company_name_extendedstatus',
                            'emitent_ukr_fullname_extendedstatus',
                            'en_name_extendedstatus',
                            'graduationYear_extendedstatus',
                            'incomeSource_extendedstatus',
                            'manufacturerName_extendedstatus',
                            'model_extendedstatus',
                            'name_extendedstatus',
                            'objectType_extendedstatus',
                            'organization_eng_company_name_extendedstatus', 'organization_ua_company_name_extendedstatus', 'organization_ukr_company_name_extendedstatus',
                            'otherObjectType_extendedstatus',
                            'owningDate_extendedstatus',
                            'propertyDescr_extendedstatus',
                            'sizeAssets_extendedstatus',
                            'sizeIncome_extendedstatus',
                            'source_eng_company_name_extendedstatus',
                            'source_ua_company_name_extendedstatus',
                            'source_ukr_company_name_extendedstatus',
                            'totalArea_extendedstatus',
                            'trademark_extendedstatus',
                            "costDate_extendedstatus",
"owningDate_extendedstatus",
"totalArea_extendedstatus",
"source_ua_company_name_extendedstatus",
"percent-ownership_extendedstatus",
"costAssessment_extendedstatus"])
    
           
    for step in [i for i in list(decl['data'].keys()) if i not in ['step_0', 'step_1']]:
        
        # print(step)
        
        if isinstance(decl['data'][step], dict):
        
            if 'empty' not in set(decl['data'][step].keys()):
            
                for step_object in decl['data'][step].keys():
                    
                    #print("step_object: " + step_object)
                    
                    if isinstance(decl['data'][step][step_object], dict):
                    
                        for step_object_field in decl['data'][step][step_object].keys():
                            
                            #print("step_object_field: " + step_object_field)
                            
                            if step_object_field == "rights":
                                
                                for right in decl['data'][step][step_object]["rights"].keys():
                                    
                                    #print("right: " + right)
                                    
                                    for right_field in decl['data'][step][step_object]["rights"][right]:
                                        
                                        #print("right_field: " + right_field)
                                        
                                        if right_field in fields_names_to_check:
                                    
                                            if decl['data'][step][step_object]["rights"][right][right_field] == "3":
                                        
                                                flag = True
                                                break
                                        
                                        
                                
                            else:
                                
                                if step_object_field in fields_names_to_check:
                                    
                                    if decl['data'][step][step_object][step_object_field] == "3":
                                        
                                        flag = True
                                        break
            
    
    return flag == ans


def flag_vehicle_purch_no_cost(decl, ans):
    
    # https://github.com/excieve/dragnet/issues/46
    
    import datetime
    
    flag = False
    
    if 'empty' not in set(decl['data']['step_6'].keys()):
        
        for k in decl['data']['step_6'].keys():
            
            if len(decl['data']['step_6'][k]['owningDate']) == 10:
                
                if int(decl['data']['step_6'][k]['owningDate'][6:]) > 0:
            
                    if datetime.datetime.strptime(decl['data']['step_6'][k]['owningDate'], "%d.%m.%Y").year == str_to_float(decl['data']['step_0']['declarationYear1']):
                    
                        if str(decl['data']['step_6'][k]['costDate']) in ['', '0']:    
                                
                            for right in decl['data']['step_6'][k]['rights'].keys():
                                
                                declarant_and_family = list(decl['data']['step_2'].keys()) + ['1'] if isinstance(decl['data']['step_2'], dict) else ['1']
    
                                if right in declarant_and_family:
                                
                                    if decl['data']['step_6'][k]['rights'][right]['ownershipType'] in ['Власність', 'Спільна власність']:
                                                    
                                        flag = True
                                        break

    
    return flag == ans


def flag_estate_purch_no_cost(decl, ans):
    
    # https://github.com/excieve/dragnet/issues/45
    
    import datetime
    
    flag = False
    
    if 'empty' not in set(decl['data']['step_3'].keys()):
        
        for k in decl['data']['step_3'].keys():
            
            if len(decl['data']['step_3'][k]['owningDate']) == 10:
                
                if int(decl['data']['step_3'][k]['owningDate'][6:]) > 0:
            
                    if datetime.datetime.strptime(decl['data']['step_3'][k]['owningDate'], "%d.%m.%Y").year == str_to_float(decl['data']['step_0']['declarationYear1']):
                    
                        if str(decl['data']['step_3'][k]['costDate']) in ['', '0']:
                            
                            if str(decl['data']['step_3'][k]['costAssessment']) in ['', '0']:        
                                
                                for right in decl['data']['step_3'][k]['rights'].keys():
                                    
                                    declarant_and_family = list(decl['data']['step_2'].keys()) + ['1'] if isinstance(decl['data']['step_2'], dict) else ['1']
        
                                    if right in declarant_and_family:
                                    
                                        if decl['data']['step_3'][k]['rights'][right]['ownershipType'] in ['Власність', 'Спільна власність']:
                                                        
                                            flag = True
                                            break

    
    return flag == ans


def flag_liabilities_to_inc_and_assets(decl, income_and_assets_sum, exchange_rates_df):
    
    # https://github.com/excieve/dragnet/issues/48
    
    total_liabilities = 0.0
    
    if 'empty' not in decl['data']['step_13'].keys():
                
        for k in decl['data']['step_13'].keys():
            
            if len(decl['data']['step_13'][k]['guarantor_realty']) == 0:
                
                if decl['data']['step_13'][k]["currency"] in set(exchange_rates_df[exchange_rates_df["year"] == str_to_float(decl['data']['step_0']['declarationYear1'])]["currency_code"]):
                
                    exchange_rate = exchange_rates_df[(exchange_rates_df["year"] == str_to_float(decl['data']['step_0']['declarationYear1'])) & (exchange_rates_df["currency_code"] == decl['data']['step_13'][k]["currency"])]["exchange_rate"].values[0]
                    
                
                else:
                    
                    exchange_rate = 1
                
                total_liabilities = total_liabilities + str_to_float(decl['data']['step_13'][k]["sizeObligation"])*exchange_rate
                    
    
    return (total_liabilities, total_liabilities >= 2*income_and_assets_sum)
