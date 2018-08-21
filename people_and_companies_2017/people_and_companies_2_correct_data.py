# You first need to run file people_and_companies_1_get_data.py

import pandas as pd

# Read the whole dataset 

p = pd.read_csv("people_and_companies_7_8_9.csv", encoding = "utf-8", sep = '|')

# Remove unnecesary cols

p = p.drop(['Unnamed: 0'], axis = 1)

# Remove all rows with NA edrpou code

p = p.loc[~p['company_id'].isnull(),:]

# Process edrpou code 
# Generally we delete all cases where length of EDRPOU code is < 4
# For Ukrainian companies - so that the length is 8 characters, if it is less, we add zeros before 

p = p[((p['company_ua'] != 1) & ((p['company_id'].str.len() >= 4)))| \
     ((p['company_ua'] == 1) & (p['company_id'].str.len() >= 4) & (p['company_id'].str.len() <= 8))]

p['company_id'].str.len().value_counts()
p[p['company_ua'] == 0]['company_id'].str.len().value_counts()

p['company_id_r'] = p['company_id']

p.loc[((p['company_ua'] == 1) & (p['company_id'].str.len() == 4)), 'company_id_r'] = '0000' + p.loc[((p['company_ua'] == 1) & (p['company_id'].str.len() == 4))]['company_id']
p.loc[((p['company_ua'] == 1) & (p['company_id'].str.len() == 5)), 'company_id_r'] = '000' + p.loc[((p['company_ua'] == 1) & (p['company_id'].str.len() == 5))]['company_id']
p.loc[((p['company_ua'] == 1) & (p['company_id'].str.len() == 6)), 'company_id_r'] = '00' + p.loc[((p['company_ua'] == 1) & (p['company_id'].str.len() == 6))]['company_id']
p.loc[((p['company_ua'] == 1) & (p['company_id'].str.len() == 7)), 'company_id_r'] = '0' + p.loc[((p['company_ua'] == 1) & (p['company_id'].str.len() == 7))]['company_id']

p[p['company_ua'] == 1]['company_id_r'].str.len().value_counts()

p['company_id_r'].str.len().value_counts()

# For a simple graph - just distinct pairs of people and companies

pairs = p.drop_duplicates(subset = ['id','company_id_r'])

# Names of companies: as there could be different wording, for each EDRPOU
# we will take the most popular option

companies_names = p[['company_id_r', "company_name", "company_ua"]]
companies_names = companies_names.groupby(['company_id_r', "company_name", "company_ua"]).size().reset_index(name='counts')
companies_names = companies_names.sort_values('counts', ascending=False).groupby('company_id_r').head(1)

# Save data

p.to_csv("p.csv", sep = "|", encoding = "utf-8")
pairs.to_csv("pairs.csv", sep = "|", encoding = "utf-8")
companies_names.to_csv("companies_names.csv", sep = "|", encoding = "utf-8")
