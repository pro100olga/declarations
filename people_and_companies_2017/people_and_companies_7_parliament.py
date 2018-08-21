# You first need to run files: 
# people_and_companies_1_get_data.py
# people_and_companies_2_correct_data.py 
# people_and_companies_3_graphs.py

import requests
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

#==============================================================================
# PARLIAMENT AND OTHERS CONNECTIONS
#==============================================================================

# This file was prepared manually in advance
# It contains members of parliament, KMU, and other top public officials
# The columns are: 'id', 'fio', 'post', 'office', 'party'

parliament = pd.read_csv("parliament_and_others.csv", sep = ";", encoding = "utf-8")

# Add president

parliament = parliament.append(pd.DataFrame({'id': ['nacp_c9e4d7dd-d6b7-44b8-9e26-12e756d36e04'],
                                             'fio': ['Порошенко Петро Олексійович'],
                                             'post': ['ПРЕЗИДЕНТ УКРАЇНИ'],
                                             'office': ['АДМІНІСТРАЦІЯ ПРЕЗИДЕНТА УКРАЇНИ'],
                                             'party': ['БПП']}))

# Create graph

g_parl = g.subgraph(list(parliament['id'])).copy()

for node1 in g_parl.nodes():
    for node2 in g_parl.nodes():
        if ((node1 != node2) & (nx.has_path(g, node1, node2))):
            if nx.shortest_path_length(g, node1, node2) <= 2:
                g_parl.add_edge(node1, node2)
                g_parl.edges[node1, node2]['path_length']= nx.shortest_path_length(g, node1, node2)
        
del node1, node2

nx.set_node_attributes(g_parl, dict(zip(list(parliament['id']), list(parliament['party']))), 'party')
nx.set_node_attributes(g_parl, dict(zip(list(parliament['id']), list(parliament['office']))), 'office')

# List with colors according to the office

color_map_office_g_parl = []

for node in list(g_parl.nodes()): 
    if  g_parl.node[node]['office'] == 'Парламент':
        color_map_office_g_parl.append('blue')
    elif  g_parl.node[node]['office'] == 'КМ':
        color_map_office_g_parl.append('green')
    elif  g_parl.node[node]['office'] == 'АДМІНІСТРАЦІЯ ПРЕЗИДЕНТА УКРАЇНИ':
        color_map_office_g_parl.append('red')
    elif  g_parl.node[node]['office'] == 'Голови ОДА':
        color_map_office_g_parl.append('orange')
    else:
        color_map_office_g_parl.append('gray')

del node

nx.draw(g_parl, 
        pos = nx.spring_layout(g_parl, k=0.5, iterations=100), 
        node_size = 20, 
        #node_size = [(nx.degree(g_parl)[node] + 1) * 20 for node in g_parl.nodes()],
        node_color = color_map_office_g_parl,
        #width = 0.1
        width = [0.2*g_parl[u][v]['path_length'] for u,v in g_parl.edges()])

plt.savefig("g_parl_and_others.png", format="PNG", dpi = 200, figsize = (8,6))

# Dataframe with 2 links (info about each of nodes which have an edge)

g_parl_edge = nx.to_pandas_edgelist(g_parl)
g_parl_edge = g_parl_edge.rename(index = str, columns = {'source': 'edge1', 'target': 'edge2'})

g_parl_edge = g_parl_edge.merge(parliament, left_on = 'edge1', right_on = 'id', how = 'left')
g_parl_edge = g_parl_edge.drop(['id'], axis=1)
g_parl_edge.rename(inplace = True,
                   columns = {'edge1': 'id1', 'edge2': 'id2', 
                              'fio': 'fio_1', 'office': 'office_1', 'party': 'party_1', 'post': 'post_1'}) 

g_parl_edge = g_parl_edge.merge(parliament, left_on = 'id2', right_on = 'id', how = 'left')
g_parl_edge = g_parl_edge.drop(['id'], axis=1)
g_parl_edge.rename(inplace = True, columns = {'fio': 'fio_2', 'office': 'office_2', 'party': 'party_2', 'post': 'post_2'}) 

g_parl_degree = pd.DataFrame({'id': list(dict(nx.degree(g_parl)).keys()),
                              'degree': list(dict(nx.degree(g_parl)).values())})

g_parl_degree = g_parl_degree[g_parl_degree['degree'] > 0]    
g_parl_degree

g_parl_edge = g_parl_edge.merge(g_parl_degree, left_on = 'id1', right_on = 'id', how = 'left')
g_parl_edge = g_parl_edge.drop(['id'], axis=1)
g_parl_edge.rename(columns={'degree':'degree_1'}, inplace=True)

g_parl_edge = g_parl_edge.merge(g_parl_degree, left_on = 'id2', right_on = 'id', how = 'left')
g_parl_edge = g_parl_edge.drop(['id'], axis=1)
g_parl_edge.rename(columns={'degree':'degree_2'}, inplace=True)

   
g_parl_edge.to_csv("g_parl_and_others_edge_df.csv", sep = "|", encoding = "utf-8")
