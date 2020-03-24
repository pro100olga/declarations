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
            
                    if datetime.datetime.strptime(decl['data']['step_3'][k]['owningDate'], "%d.%m.%Y") > datetime.datetime.strptime('01.01.2014', "%d.%m.%Y"):
                    
                        if str(decl['data']['step_3'][k]['costDate']) in ['', '0']:
                            
                            if str(decl['data']['step_3'][k]['costAssessment']) in ['', '0']:               
                            
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
                                  pattern = "приз|вигр|выигр|лотер")):
                    
                    prize_amount = prize_amount + str_to_float(s = decl['data']['step_11'][k]['sizeIncome'])
             
    if prize_amount > 10000.0:
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
            
            if len(decl['data']['step_3'][k]['totalArea']) > 0:
            
                if ((str_to_float(s = decl['data']['step_3'][k]['totalArea']) > 300) & (decl['data']['step_3'][k]['objectType'] not in ["Земельна ділянка"])):
                    
                    flag = True
                    break
            
    return flag == ans   


def flag_has_foreign_real_estate(decl, ans):
    
    # https://github.com/excieve/dragnet/issues/41
    
    flag = False
    
    if 'empty' not in set(decl['data']['step_3'].keys()):
        
        for k in decl['data']['step_3'].keys():
            
            if decl['data']['step_3'][k]['country'] != "1":
                
                flag = True
                break
            
    return flag == ans   


def flag_has_bo_abroad(decl, ans):
    
    # https://github.com/excieve/dragnet/issues/42
    
    flag = False
    
    if 'empty' not in set(decl['data']['step_9'].keys()):
        
        for k in decl['data']['step_9'].keys():
            
            if decl['data']['step_9'][k]['country'] != "1":
                
                flag = True
                break
            
    return flag == ans   


def flag_has_non_bank_liabilities(decl, ans):
    
    import re
    
    # https://github.com/excieve/dragnet/issues/38
    
    # Load file - created by code from here 
    # https://github.com/pro100olga/declarations/blob/master/bi/red_flags/liabilities_not_banks_insurance_leasing.py
    
    banks_edrpou = pd.read_csv("C:\\Users\\olga.makarova\\Downloads\\declarations\\banks_edrpou.csv")
    banks_edrpou = set(banks_edrpou['banks_edrpou'])
    
    banks_names = set(["твбв", "ощадбанк", "приватбанк", "аваль", "райффайзен", "абанк", "агріколь", "укрсиббанк", "альфабанк", "пумб", "укргазбанк", "мегабанк", "акордбанк", "сбербанк", "таскомбанк", "кредобанк", "індустріалбанк", "укрексімбанк", "радабанк", "укркомунбанк", "укрбудінвестбанк", "правексбанк", "правекс", "прокредит", "метабанк", "комінвестбанк", "форвард"])
    
    flag = False
            
    if 'empty' not in set(decl['data']['step_13'].keys()):
        
        for k in decl['data']['step_13'].keys():
            
            flag_company_code = False
            flag_ua_company_name = False
            flag_ukr_company_name = False
            
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
                        
                    
            if not flag_company_code and not flag_ua_company_name and not flag_ukr_company_name == True:
                break

        if not flag_company_code and not flag_ua_company_name and not flag_ukr_company_name == True:
            flag = True
        
    return  flag == ans
