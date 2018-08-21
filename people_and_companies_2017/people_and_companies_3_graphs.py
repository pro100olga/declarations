# You first need to run files people_and_companies_1_get_data.py, people_and_companies_2_correct_data.py 

import pandas as pd
import networkx as nx

# Read data

p = pd.read_csv("p.csv", sep = "|", encoding = "utf-8")
pairs = pd.read_csv("pairs.csv", sep = "|", encoding = "utf-8")
companies_names = pd.read_csv("companies_names.csv", sep = "|", encoding = "utf-8")

# Create graph

subset = pairs[['id', 'company_id_r']]
tuples = [tuple(x) for x in subset.values]

g = nx.Graph(tuples)

del subset, tuples

# Add node attributes

p['fio_post_comp'] = p['fio'] + ', ' + p['position'] + ', ' + p['office']
 
nodes_person = p[['id','fio_post_comp']].drop_duplicates(subset = ['id','fio_post_comp'])
nodes_person['company_ua'] = -999 
nodes_person['label'] = 'person' 
nodes_person.columns = ['id', 'name', 'company_ua', 'label']

nodes_comp = companies_names[['company_id_r', 'company_name', 'company_ua']].drop_duplicates(subset = ['company_id_r', 'company_name', 'company_ua'])
nodes_comp['label'] = 'company'
nodes_comp.columns = ['id', 'name', 'company_ua', 'label']

nodes = pd.concat([nodes_person, nodes_comp])

del nodes_person, nodes_comp

nx.set_node_attributes(g, dict(zip(list(nodes['id']), list(nodes['name']))), 'name')
nx.set_node_attributes(g, dict(zip(list(nodes['id']), list(nodes['company_ua']))), 'company_ua')
nx.set_node_attributes(g, dict(zip(list(nodes['id']), list(nodes['label']))), 'label')

