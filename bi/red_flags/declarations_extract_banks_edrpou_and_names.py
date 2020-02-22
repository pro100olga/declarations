
import requests
import string
import re
import pandas as pd

####################### BANKS NAMES AND EDRPOU CODES

# We will take data about banks from 2 APIs (bank.gov.ua and nbu.rocks) and extract EDRPOU codes and banks' names

banks1 = requests.get("https://bank.gov.ua/NBU_BankInfo/get_data_branch?&json").json()
banks2 = requests.get("http://nbu.rocks/jsons/complete.json").json()

# banks1 = banks1['rcukru']['rowrcukru'] # extract list of banks

# Create a list of EDRPOU codes

banks_edrpou = []
banks_names = []

for i in range(len(banks1)): # add all codes from 1st list, convert them to single type - string

    # Long bank name 
    banks_names.append(re.sub(' +',' ', banks1[i]['N_GOL'].lower().translate(str.maketrans('', '', string.punctuation)).strip())) # remove all punctuation, double spaces and trail spaces, lowercase
      
    # Short bank name 
    banks_names.append(re.sub(' +',' ', banks1[i]['SHORTNAME'].lower().translate(str.maketrans('', '', string.punctuation)).strip())) # remove all punctuation, double spaces and trail spaces, lowercase
    
    # EDRPOU code   
    banks_edrpou.append(str(banks1[i]['KOD_EDRPOU']))


for i in range(len(banks2)): # add all codes from 2nd list, convert them to single type - string

    # Bank name 
    banks_names.append(re.sub(' +',' ', banks2[i]['Ліцензії'][0]['Назва банку'].lower().translate(str.maketrans('', '', string.punctuation)).strip())) # remove all punctuation, double spaces and trail spaces, lowercase
   
    # EDRPOU code
    banks_edrpou.append(str(banks2[i]['Ліцензії'][0]['Код ЄДРПОУ']))

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
